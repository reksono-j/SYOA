import os
import json
from singleton import Singleton

class EditorVariableManager(metaclass=Singleton):
    def __init__(self, path=None):
        self.Variables = {}

        if path is None:
            path = os.path.dirname(os.path.abspath(__file__)) 
        path = os.path.join(path, 'variables.json')  
        self.path = path 
        if path:
            self.loadVariables()  

    def setVariable(self, name, value):
        if self.isValidName(name):
            self.Variables[name.lower()] = value  
            self.saveVariables()  
            return True
        return False

    def isKey(self, name):
        if name in self.Variables:
            return True
        return False
    
    def deleteVariable(self, name):
        if name.lower() in self.Variables:
            del self.Variables[name.lower()]
            self.saveVariables()

    def listVariables(self):
        return self.Variables.items()

    def isValidName(self, name):
        return name.isidentifier() and name[0].isalpha()  

    def saveVariables(self):
        with open(self.path, 'w') as f:  
            json.dump(self.Variables, f)

    def loadVariables(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:  
                self.Variables = json.load(f)

    def clearVariables(self):
        self.Variables = {}