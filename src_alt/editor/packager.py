from sceneStructure import *
from pathlib import Path
from parser import readScript
from zipfile import ZipFile
from variableManager import EditorVariableManager
from characterManager import CharacterManager
from backgroundManager import BackgroundManager
from projectManager import ProjectManager
import io, os
import json
from textToSpeech import TTS, VOICE


class StoryPackager:
    counter = 0
    def __init__(self):
        self.sceneNames = [] # For validation
        self.rawScenes = [] # To be serialized
        self.SoundData = [] # To be have audio generated
        self.assets = [] 
        self.startingScene = ""
        self.variableManager = EditorVariableManager()
        self.characterManager = CharacterManager()
        self.backgroundManager = BackgroundManager()
        self.projectManager = ProjectManager()
        
    def _checkVariable(self, variable: str, intPossible = True):
        if variable.isidentifier():
            
            if self.variableManager.isKey(variable):
                variable = variable.lower()
                return f"self.vm.get('{variable}')"
            else:
                raise ValueError(f"ERROR: variable {variable} doesn't exist")
        elif (intPossible):
            try:
                int(variable)
                return variable
            except:
                raise TypeError(f"ERROR: variable {variable} is not integer")
        else:
            raise ValueError(f"ERROR: variable {variable} doesn't exist")
    
            
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
            data = self.characterManager.getAliasInfo(name)
            if data:
                return data
            else:
                raise ValueError(f"ERROR: Unknown alias {name}")
        else:
            return {}    
    
    def _checkAsset(self, name:str, type:str):
        match(type):
            case "bgm":
                return self._CheckAudio(name, "BGM")
            case "sfx":
                return self._CheckAudio(name, "SFX")
            case "bg":
                if self.backgroundManager.backgroundExists(name):
                    return self.backgroundManager.getBackgroundFilePathByBaseName(name)
                raise FileNotFoundError(f"ERROR: Background {name} does not exist")
    
    def _CheckAudio(self, audio, sceneTitle):
        projectPath = self.projectManager.getCurrentFilePath()
        audioPathWithoutScene = Path(os.path.join(projectPath, 'audio', audio))
        audioPathWithScene = Path(os.path.join(projectPath, 'audio', sceneTitle, audio))
        if audioPathWithoutScene.exists():
            audioPath = str(audioPathWithoutScene.resolve())
        else:
            if audioPathWithScene.exists():
                audioPath = str(audioPathWithScene.resolve())
            else:
                raise FileNotFoundError(f'ERROR: Audio file "{audio}" not found')
        return audioPath
        
    def _serializeElement(self, el: Element, sceneTitle: str):
        if type(el) == Dialogue:
            self.counter += 1
            dialogue = {}
            speaker = self._checkCharacter(el.speaker)
            if 'name' in speaker:
                speaker = speaker['name']
            if not any(char.isalnum() for char in el.text):
                dialogue = {"type":"dialogue", "speaker":speaker, "text":el.text, "audio": el.audio} 
            else:
                if el.audio == '':
                    if 'voice' in speaker:
                        dialogue = {"type":"dialogue", "speaker":speaker, "text":el.text, "audio": f"audio/{sceneTitle}/{self.counter}.wav"}
                    else:
                        dialogue = {"type":"dialogue", "speaker":speaker, "text":el.text, "audio": f"audio/{sceneTitle}/{self.counter}.wav"}
                else:
                    audio = self._CheckAudio(el.audio, sceneTitle)                    
                    parentFolder = os.path.basename(os.path.dirname(audio)) 
                    fileName = os.path.basename(audio) 
                    archivePath = f"audio/{parentFolder}/{fileName}"
                    dialogue = {"type":"dialogue", "speaker":speaker, "text":el.text, "audio": archivePath, "path": audio}
            self.SoundData.append(dialogue)
            return dialogue
        if type(el) == Modify:
            action = ""
            var = self._checkVariable(el.variable, False)            
            match(el.operation):
                case Operation.ADD:
                    action = f"self.vm.set('{el.variable}', {var} + {el.amount})"
                case Operation.SUB:
                    action = f"self.vm.set('{el.variable}', {var} - {el.amount})"
                case Operation.SET:
                    action = f"self.vm.set('{el.variable}', {el.amount})"
                case Operation.MOD:
                    action = f"self.vm.set('{el.variable}', {var} % {el.amount})"
            var = var.lower()
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
                raise FileNotFoundError("ERROR: Scene does not exist")
            return {"type":"branch", "next": el.scene}
        if type(el) == Asset:
            path = self._checkAsset(el.fileName, el.type)
            if path:               
                parentFolder = os.path.basename(os.path.dirname(path)) 
                fileName = os.path.basename(path) 
                archivePath = f"{parentFolder}/{fileName}"
                if el.type == "sfx" or el.type == "bgm":
                    asset = {"type": el.type, "file":el.fileName, "option": el.options, "absPath": path, "path": f'audio/{archivePath}'}
                else:
                    asset = {"type": el.type, "file":el.fileName, "option": el.options, "absPath": path, "path": archivePath}
                self.assets.append(asset.copy())
                asset.pop('absPath')
                return asset
            else:
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
            totalTasks = len(self.rawScenes) + len(self.SoundData) + 2 + 5 # Scenes + Audio + Metadata & Variables + Writing
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
                
                
                arcnames = []
                # Generate and add audio files
                for line in self.SoundData:
                    if "audio" in line:
                        if line['audio'] not in arcnames:
                            if "path" in line:
                                file.write(line['path'] , arcname=line['audio']) 
                                
                            else:
                                if line['audio'] != "":
                                    speaker = line['speaker']
                                    if 'voice' in speaker:
                                        TTS.setSpeaker(VOICE[speaker['voice']])
                                    else:
                                        TTS.setSpeaker(VOICE.female1)
                                    audioBuffer = TTS.convertToAudio(line["text"])
                                    file.writestr(line["audio"], audioBuffer.getvalue())
                            arcnames.append(line['audio'])
                            
                    currentTask += 1
                    updateProgress()
                
                for asset in self.assets:
                    print(asset)
                    if asset['path'] not in arcnames:
                        file.write(asset['absPath'] , arcname=asset['path']) 
                        arcnames.append(asset['path'])
                            

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
            print(f"Error during serialization: {type(e)} {e}")
            raise Exception(e)
                