from sceneStructure import *
from pathlib import Path
from parser import readScript
from zipfile import ZipFile
from variableManager import VariableManager
import io
import json


import wave
import math

# TODO: Create a some sort of setting that stores the project folder path and references it in this file
storyDirectory = Path("src/editor/parser/Story_EX_DeleteLater")

class storyPackager:
    counter = 0
    def __init__(self):
        self.sceneNames = [] # For validation
        self.rawScenes = [] # To be serialized
        self.Dialogue = [] # To be have audio generated
    
    def _checkVariable(self, variable: str):
        if variable.isidentifier():
            vm = VariableManager()
            if vm.isKey(variable):
                return f"<VariableManager>[{variable}]"
            else:
                print("ERROR This variable doesn't exist") # TODO error checking here to stop compilatin
        else:
            try:
                int(variable)
                return variable
            except:
                print("ERROR") # TODO ERR CHECKING
            
    def loadStoryFiles(self):
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
            dialogue = {"type":"dialogue", "speaker":el.speaker, "text":el.text, "audio": f"audio/{sceneTitle}/{self.counter}.wav"} #TODO I have it set to wave files instead of mp3s because of the wave package being built-in
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
                choice = {}
                choice["text"] = option.text
                choice["lines"] = []
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
    
    
    # TODO : I'm currently using some example code from https://realpython.com/python-wav-files/ to make the files
    FRAMES_PER_SECOND = 44100

    def sound_wave(self, frequency, num_seconds):
        for frame in range(round(num_seconds * self.FRAMES_PER_SECOND)):
            time = frame / self.FRAMES_PER_SECOND
            amplitude = math.sin(2 * math.pi * frequency * time)
            yield round((amplitude + 1) / 2 * 255)

    def serializeScenes(self):
        buffer = io.BytesIO()
        with ZipFile(buffer, 'w') as file:
            # Reads each scene file
            for scene in self.rawScenes:
                sceneData = self._serializeScene(scene)
                file.writestr(f"scripts/{sceneData["title"]}", json.dumps(sceneData, indent = 2))
                
            # TODO: Add the actual TTS audio creation
            # Temporary Audio creation
            for line in self.Dialogue:
                waveBuffer = io.BytesIO()
                with wave.open(waveBuffer, mode="wb") as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(1)
                    wav_file.setframerate(self.FRAMES_PER_SECOND)
                    wav_file.writeframes(bytes(self.sound_wave((1 + (abs(hash(line["text"])) % 1000)), 2.5)))
                waveBuffer.seek(0)
                file.writestr(line["audio"], waveBuffer.read())

        # TODO: Give actual name instead of testStory.zip
        # Writes buffer contents to actual zip
        buffer.seek(0) 
        with open("src/viewer/Story_EX_DeleteLater/testStory.syoa", "wb") as zipFile:
            zipFile.write(buffer.read())
        



            


if __name__ == "__main__":
    vm = VariableManager()
    vm['rock'] = 10
    compiler = storyPackager()
    compiler.loadStoryFiles()
    compiler.serializeScenes()
    #compiler.serializeManagerData()