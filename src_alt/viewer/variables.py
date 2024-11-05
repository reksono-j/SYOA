import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget
)
from PySide6.QtCore import Qt
from singleton import Singleton

# TODO: Make this reset when opening a new project
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
    
    def loadFromSavefile(self, savePath):
        if os.path.exists(savePath):
            with open(savePath, 'r') as f:
                data = json.load(f)
                self.Variables = data.get('variables', {}) 
        
    def loadInitialVariables(self,data):
        self.Variables = json.load(data)


class VariableViewerGUI(QWidget):
    def __init__(self, path='variables.json'):
        super().__init__()

        self.vm = ViewerVariableManager(path)  
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Variable Viewer')
        self.setGeometry(100, 100, 500, 400) # TODO : Figure out what to make the dimensions
        layout = QVBoxLayout()

        self.variableList = QListWidget()
        self.variableList.setFocusPolicy(Qt.StrongFocus)  
        layout.addWidget(self.variableList)

        
        self.exitButton = QPushButton('Exit')
        self.exitButton.clicked.connect(self.close)
        layout.addWidget(self.exitButton)

        self.setLayout(layout)
        self.listVariables()  

        if self.variableList.count() > 0:
            self.variableList.setCurrentRow(0)

    def listVariables(self):
        self.variableList.clear()  
        for name, value in self.vm.listVariables():
            self.variableList.addItem(f"{name}: {value}")


    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            
            if self.exitButton.hasFocus():
                self.close()  
            else:
                item = self.variableList.currentItem()  
                if item:
                    self.openEditDialog(item)  
        elif event.key() == Qt.Key_Escape:
            self.exitButton.setFocus()  
        else:
            super().keyPressEvent(event)  