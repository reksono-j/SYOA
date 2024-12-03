import json, os
from src.viewer.singleton import Singleton

class ViewerVariableManager(metaclass=Singleton):
    def __init__(self, path=None):
        self.Variables = {}
        
        if path is None:
            scriptDir = os.path.dirname(os.path.abspath(__file__)) 
            path = os.path.join(scriptDir, 'variables.json')
        self.path = path 

    def set(self, name, value):
        self.Variables[name.lower()] = value 
    
    def get(self, name):
        return self.Variables[name.lower()]
        
    def listVariables(self):
        return self.Variables.items()

    def getVariables(self):
        return self.Variables
    
    def isValidName(self, name):
        return name.isidentifier() and name[0].isalpha()
    
    def loadFromDict(self, data:dict):
        self.Variables = data
        
    def loadInitialVariables(self,data):
        self.Variables = json.load(data)
