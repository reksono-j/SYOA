from speakerForm import *
from singleton import Singleton

class VariableManager(metaclass = Singleton):
    variables = {}
    def __init__(self):
        pass

    def __getitem__(self, key):
        return self.variables[key]
    
    def __setitem__(self, key, value):
        self.variables[key] = value
    
    def __delitem__(self, key):
        del self.variables[key]
    
    def updateName(self, oldName: str, newName: str):
        if oldName in self.variables:
            self.variables[newName] = self.variables.pop(oldName)
        else:
            print(f"{oldName} was not found.")
        
    def isKey(self, name):
        return name in self.variables

    

if __name__ == "__main__":
    vm1 = VariableManager()
    vm1['rock'] = 10
    vm2 = VariableManager()
    print(vm2['rock'])