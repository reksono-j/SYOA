import os, json
from singleton import Singleton
from pathlib import Path
import platform


class FileManager(metaclass=Singleton):
    def __init__(self):
        if platform.system() == 'Windows':
            self.dataFolder = Path(os.getenv('LOCALAPPDATA'))/'SYOA'
        elif platform.system() == 'Darwin':  # macOS
            self.dataFolder = Path.home()/'Library'/'Application Support'/'SYOA'
        else: # Linux
            self.dataFolder = Path.home()/'.config'/'SYOA'
    
        if not self.dataFolder.exists():
            self.createDataFolder()

    def getFilepath(self):
        return self.dataFolder
        
    def createDataFolder(self,):
        if not self.dataFolder.exists():
            try:
                self.dataFolder.mkdir(parents=True, exist_ok=False)
                saveDataFolder = self.dataFolder/'Save'
                saveDataFolder.mkdir(parents=True, exist_ok=False)
            except Exception as e:
                print(f"Failed to create folder: {e}")
        else:
            print(f"User data folder already exists: {self.dataFolder}")


    def createSaveFile(self, filename: str, data: dict):
        saveDataFolder = self.dataFolder/'Save'
        try:
            if not saveDataFolder.exists():
                saveDataFolder.mkdir(parents=True, exist_ok=False)
        except Exception as e:
            print(f"Failed to create folder: {e}")

        filepath = saveDataFolder / filename
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Failed to write save file: {e}")
    
    def readSaveFile(self, filepath:str) -> dict:
        data = None
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f"Failed to read save file: {e}")
        return data
        
    