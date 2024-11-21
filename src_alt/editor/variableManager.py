import os
import json
from src_alt.editor.singleton import Singleton
from src_alt.editor.projectManager import ProjectManager

class EditorVariableManager(metaclass=Singleton):
    def __init__(self):
        self.projectManager = ProjectManager()
        self.Variables = {}
        
        self.projectManager.changedProject.connect(self.updatePath)
        self.updatePath()

    def updatePath(self):
        path = self.projectManager.getCurrentFilePath()
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

    def get(self, name):
        if name.lower() in self.Variables:
            return self.Variables[name.lower()]
        print("ERROR: Variable doesn't exist")
    
    def isKey(self, name):
        if name.lower() in self.Variables:
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
        self.clearVariables()
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:  
                self.Variables = json.load(f)

    def clearVariables(self):
        self.Variables.clear()