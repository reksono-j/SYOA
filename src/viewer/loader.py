import json, os
import zipfile
from src.viewer.variables import ViewerVariableManager
from src.viewer.singleton import Singleton

class Loader(metaclass=Singleton):
    def __init__(self):
        self._sceneFilePaths = {}
        self._audioFilePaths = {}
        self._package = "" # Project File Path
        self._data = {}
        self.projectLoaded = False
    
    def setProject(self, filePath: str):
        self._package = filePath
        self.projectLoaded = True
    
    def loadPackage(self):
        self._readVariablesIntoManager()
        self._readStoryFilePaths()
        self._readMetadata()
        
    def _readStoryFilePaths(self):
        with zipfile.ZipFile(self._package, 'r') as file:
            for item in file.infolist():
                if not item.is_dir():
                    if item.filename.startswith('scripts/'):
                        #self.audioFilePaths[Path(item.filename).name]
                        pathParts = item.filename.split('/')
                        sceneName = pathParts[1]
                        sceneName, ext = os.path.splitext(sceneName)
                        self._sceneFilePaths[sceneName] = item.filename
                    elif item.filename.startswith('audio/'):
                        pathParts = item.filename.split('/')
                        audioName = pathParts[1]
                        audioName, ext = os.path.splitext(audioName)
                        if not audioName in self._audioFilePaths:
                            self._audioFilePaths[audioName] = []
                        self._audioFilePaths[audioName].append(item.filename)
    
    def _readVariablesIntoManager(self):
        with zipfile.ZipFile(self._package, 'r') as file:
            with file.open('variables.json') as data:
                vm = ViewerVariableManager()
                vm.loadInitialVariables(data)
    
    def _readMetadata(self):
        with zipfile.ZipFile(self._package, 'r') as file:
            with file.open('data') as data:
                self._data = json.load(data)
    
    def readSceneToJSONString(self, sceneName: str) -> str: 
        with zipfile.ZipFile(self._package, 'r') as file:
            with file.open(self._sceneFilePaths[sceneName]) as scene:
                return scene.read().decode('utf-8')

    def readSceneToDict(self, sceneName: str):
        return json.loads(self.readSceneToJSONString(sceneName))

    def getPackagePath(self):
        return self._package
    
    def getID(self) -> str: 
        return self._data['id']
    
    def getStartScene(self) -> str:
        return self._data['start']
    
    
    def projectLoaded(self):
        return self.projectLoaded
            
