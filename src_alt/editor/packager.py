from sceneStructure import *
from pathlib import Path
from parser import readScript
from zipfile import ZipFile
from variableManager import EditorVariableManager
from characterManager import CharacterManager
import io
import json
from textToSpeech import TTS


class StoryPackager:
    counter = 0
    def __init__(self):
        self.sceneNames = [] # For validation
        self.rawScenes = [] # To be serialized
        self.Dialogue = [] # To be have audio generated
        self.startingScene = ""
        
        
    def _checkVariable(self, variable: str):
        if variable.isidentifier():
            vm = EditorVariableManager()
            if vm.isKey(variable):
                variable = variable.lower()
                return f"self.vm.get('{variable}')"
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
        self.variablesPath = storyDirectory.joinpath('variables.json')
        for path in storyDirectory.iterdir():
            if path.name.endswith('.txt'):
                sceneName = path.name.removesuffix('.txt')
                self.sceneNames.append(sceneName)
                if path.is_file():	
                    with open(path, 'r') as file:
                        script = file.read()
                        scene = readScript(script)
                        scene.title = sceneName
                        self.rawScenes.append(scene)
            
            if path.name.endswith('.json'):
                if path.name == 'variables.json':
                    with open(path, 'r', encoding='utf-8') as file:
                        self.rawVars = file.read()
                if path.name == 'project.json':
                    with open(path, 'r', encoding='utf-8') as file:
                        self.ID = json.loads(file.read())["id"]
                
    def _checkCharacter(self, name: str):
        if name:
            cm = CharacterManager()
            data = cm.getAliasInfo(name)
            if data:
                return data
            else:
                print(f"ERROR: Unknown alias {name}") # TODO exception
                return ""
        else:
            return {}    
    
    def _serializeElement(self, el: Element, sceneTitle: str):
        if type(el) == Dialogue:
            self.counter += 1 # TODO : Add character manager speaker id validation
            dialogue = {}
            speaker = self._checkCharacter(el.speaker)
            if not any(char.isalnum() for char in el.text):
                dialogue = {"type":"dialogue", "speaker":speaker, "text":el.text} 
            else:
                dialogue = {"type":"dialogue", "speaker":speaker, "text":el.text, "audio": f"audio/{sceneTitle}/{self.counter}.wav"}
                
            self.Dialogue.append(dialogue)
            return dialogue
        if type(el) == Modify:
            action = ""
            el.variable = el.variable.lower()
            match(el.operation):
                case Operation.ADD:
                    action = f"self.vm.set('{el.variable}', self.vm.get('{el.variable}') + {el.amount})"
                case Operation.SUB:
                    action = f"self.vm.set('{el.variable}', self.vm.get('{el.variable}') - {el.amount})"
                case Operation.SET:
                    action = f"self.vm.set('{el.variable}', {el.amount})"
                case Operation.MOD:
                    action = f"self.vm.set('{el.variable}', self.vm.get('{el.variable}') % {el.amount})"
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
            for i, option in enumerate(el.options, 1):
                choice = {"text": option.text, "index":i, "lines": []}
                for lineElement in option.consequences:
                    choice["lines"].append(self._serializeElement(lineElement, sceneTitle))
                choices.append(choice)
            return {"type":"choice", 'choices': choices}
        if type(el) == Branch:
            if not (el.scene in self.sceneNames):
                print("ERROR: Scene does not exist") # TODO ERR CHECKING
            return {"type":"branch", "next": el.scene}
        if type(el) == Asset: # TODO: add verification that the files exist
            return {"type": el.type, "file":el.fileName, "option": el.fileName}
                
    
    def _serializeScene(self, scene: Scene):
        self.counter = 0
        lines = []
        for element in scene.lines:
            lines.append(self._serializeElement(element, scene.title))
        return {"title": scene.title, "lines": lines, "links": scene.links}
    
    def setStartingScene(self, sceneName: str):
        self.startingScene = sceneName
    
    
    def serializeScenes(self, filepath, progressCallback=None):
        try:
            totalTasks = len(self.rawScenes) + len(self.Dialogue) + 2 + 5 # Scenes + Audio + Metadata & Variables + Writing
            currentTask = 0

            def updateProgress():
                if progressCallback:
                    progressCallback(int((currentTask / totalTasks) * 100))

            buffer = io.BytesIO()
            with ZipFile(buffer, 'w') as file:
                # Reads each scene file
                for scene in self.rawScenes:
                    sceneData = self._serializeScene(scene)
                    file.writestr(f"scripts/{sceneData['title']}.json", json.dumps(sceneData, indent=2))
                    currentTask += 1
                    updateProgress()

                # Generate and add audio files
                for line in self.Dialogue:
                    if "audio" in line:
                        audioBuffer = TTS.convertToAudio(line["text"])
                        file.writestr(line["audio"], audioBuffer.getvalue())
                    currentTask += 1
                    updateProgress()

                # Write metadata and variables
                file.writestr("data", json.dumps({"start": self.startingScene, "id": self.ID}, indent=2))
                currentTask += 1
                updateProgress()

                file.writestr("variables.json", self.rawVars)
                currentTask += 1
                updateProgress()

            # Writes buffer contents to the actual zip file
            buffer.seek(0)
            with open(filepath, "wb") as zipFile:
                zipFile.write(buffer.read())
            
            currentTask += 5
            updateProgress()
            
            return True
        except Exception as e:
            print(f"Error during serialization: {e}")
            return False