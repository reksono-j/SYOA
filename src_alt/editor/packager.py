from sceneStructure import *
from pathlib import Path
from parser import readScript
from zipfile import ZipFile
from variableManager import EditorVariableManager
import io
import json
import math
from textToSpeech import TTS


class StoryPackager:
    counter = 0
    def __init__(self):
        self.sceneNames = [] # For validation
        self.rawScenes = [] # To be serialized
        self.Dialogue = [] # To be have audio generated
        self.startingScene = ""
    
    @staticmethod
    def _checkVariable(variable: str):
        if variable.isidentifier():
            vm = EditorVariableManager()
            if vm.isKey(variable):
                return f"<VariableManager>[{variable}]"
            else:
                print(f"ERROR: variable {variable} doesn't exist") # TODO error checking here to stop compilatin
        else:
            try:
                int(variable)
                return variable
            except:
                print("ERROR") # TODO ERR CHECKING
            
    def loadStoryFiles(self, projectDirectory):
        storyDirectory = Path(projectDirectory)
        for path in storyDirectory.iterdir():
            sceneName = path.name.removesuffix('.txt')
            self.sceneNames.append(sceneName)
            if path.is_file():	
                with open(path, 'r') as file:
                    script = file.read()
                    scene = readScript(script)
                    scene.title = sceneName
                    self.rawScenes.append(scene)
    
    def _serializeElement(self, el: Element, sceneTitle: str):
        if type(el) == Dialogue:
            self.counter += 1 # TODO : Add character manager speaker id validation
            dialogue = {}
            if not any(char.isalnum() for char in el.text):
                dialogue = {"type":"dialogue", "speaker":el.speaker, "text":el.text} 
            else:
                dialogue = {"type":"dialogue", "speaker":el.speaker, "text":el.text, "audio": f"audio/{sceneTitle}/{self.counter}.wav"}
                
            self.Dialogue.append(dialogue)
            return dialogue
        if type(el) == Modify:
            action = f"<VariableManager>[{el.variable}] "
            match(el.operation):
                case Operation.ADD:
                    action += "+= "
                case Operation.SUB:
                    action += "-= "
                case Operation.SET:
                    action += "= "
                case Operation.MOD:
                    action += "%= "
            action +=  f"{el.amount}"
            return {"type":"modify", "action": action}
        if type(el) == Conditional:    
            conditional = {}
            var1 = self._checkVariable(el.var1)
            var2 = self._checkVariable(el.var2)
            comparison = var1 + " "
            match(el.compare):
                case Comparator.LESS:
                    comparison += "< "
                case Comparator.MORE:
                    comparison += "> "
                case Comparator.EQ:
                    comparison += "== "
                case Comparator.LTE:
                    comparison += "<= "
                case Comparator.MTE:
                    comparison += ">= "
            comparison += var2
            conditional['comparison'] = comparison
            conditional['ifLines'] = []
            conditional['elseLines'] = []
            for lineElement in el.ifElements:
                conditional['ifLines'].append(self._serializeElement(lineElement, sceneTitle))
            for lineElement in el.elseElements:
                conditional['elseLines'].append(self._serializeElement(lineElement, sceneTitle))
            conditional['type'] = "conditional"
            return conditional
        if type(el) == Choice:
            choices =  []
            for option in el.options:
                choice = {"text": option.text, "lines": []}
                for lineElement in option.consequences:
                    choice["lines"].append(self._serializeElement(lineElement, sceneTitle))
                choices.append(choice)
            return {"type":"choice", 'choices': choices}
        if type(el) == Branch:
            if not (el.scene in self.sceneNames):
                print("ERROR: Scene does not exist") # TODO ERR CHECKING
            return {"type":"branch", "next": el.scene}
    
    def _serializeScene(self, scene: Scene):
        self.counter = 0
        lines = []
        for element in scene.lines:
            lines.append(self._serializeElement(element, scene.title))
        return {"title": scene.title, "lines": lines, "links": scene.links}
    
    def setStartingScene(self, sceneName: str):
        self.startingScene = sceneName
    
    def serializeScenes(self, filepath):
        try:
            buffer = io.BytesIO()
            with ZipFile(buffer, 'w') as file:
                # Reads each scene file
                for scene in self.rawScenes:
                    sceneData = self._serializeScene(scene)
                    file.writestr(f"scripts/{sceneData["title"]}", json.dumps(sceneData, indent = 2))
                    
                for line in self.Dialogue:
                    if "audio" in line:
                        audioBuffer = TTS.convertToAudio(line["text"])
                        file.writestr(line["audio"], audioBuffer.getvalue())
                
                file.writestr(f"data", json.dumps({"start": self.startingScene}))
                
            # Writes buffer contents to actual zip
            buffer.seek(0) 
            with open(filepath, "wb") as zipFile:
                zipFile.write(buffer.read())
            return True
        except:
            return False
        



            


if __name__ == "__main__":
    vm = EditorVariableManager()
    vm.setVariable("rock", 10)
    compiler = StoryPackager()
    compiler.loadStoryFiles()
    compiler.serializeScenes()
    #compiler.serializeManagerData()