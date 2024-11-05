import json
import zipfile
from pathlib import Path
from variables import ViewerVariableManager

projectPath = Path("SYOA/src/viewer/Story_EX_DeleteLater")

# TODO : Possibly make this into a singleton
class Loader():
    def __init__(self):
        self._sceneFilePaths = {}
        self._audioFilePaths = {}
        self._package = ""
    
    def setProject(self, filePath: str):
        self._package = filePath
    
    def readStoryFilePaths(self):
        with zipfile.ZipFile(self._package, 'r') as file:
            for item in file.infolist():
                if not item.is_dir():
                    if item.filename.startswith('scripts/'):
                        #self.audioFilePaths[Path(item.filename).name]
                        pathParts = item.filename.split('/')
                        sceneName = pathParts[1]
                        self._sceneFilePaths[sceneName] = item.filename
                    elif item.filename.startswith('audio/'):
                        pathParts = item.filename.split('/')
                        sceneName = pathParts[1]
                        if not sceneName in self._audioFilePaths:
                            self._audioFilePaths[sceneName] = []
                        self._audioFilePaths[sceneName].append(item.filename)

    def readVariablesIntoManager(self):
        with zipfile.ZipFile(self._package, 'r') as file:
            with file.open('variables.json') as data:
                vm = ViewerVariableManager()
                vm.loadInitialVariables(data)
        
    def getStartScene(self):
        with zipfile.ZipFile(self._package, 'r') as file:
            with file.open('data') as scene:
                return json.loads(scene.read().decode('utf-8'))['start']
    
    def readSceneToJSONString(self, sceneName: str) -> str: 
        with zipfile.ZipFile(self._package, 'r') as file:
            with file.open(self._sceneFilePaths[sceneName]) as scene:
                return scene.read().decode('utf-8')

    def readSceneToDict(self, sceneName: str):
        return json.loads(self.readSceneToJSONString(sceneName))

    def getPackagePath(self):
        return self._package
    
if __name__ == "__main__":
    loader = Loader()
    loader.setProject(projectPath.joinpath("testStory.syoa"))
    loader.readStoryFilePaths()
    print(loader.readSceneToJSONString("Scene1"))
    #print(loader.readSceneToDict("Scene1"))
    
