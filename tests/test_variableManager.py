import unittest
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit
)
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
import json
import copy
import os
from pathlib import Path
import sys
import shutil
import json


from src_alt.editor import variableManager
from src_alt.editor.projectManager import ProjectManager

class Test(unittest.TestCase):
    def setUp(self):
        workingDir = os.path.dirname(os.path.abspath(__file__))
        parent_path = os.path.dirname(workingDir)
        self.projectM = ProjectManager(parent_path)
        self.projectM.createProject("variableManagerProject")
        self.testProjectDir = os.path.join(parent_path, "variableManagerProject")
        self.varM = variableManager.EditorVariableManager()
        
        return super().setUp()
    
    def tearDown(self):
        try:
            shutil.rmtree(self.testProjectDir)
            print(f"Directory '{self.testProjectDir}' deleted successfully.")
        except FileNotFoundError:
            print(f"Directory '{self.testProjectDir}' not found.")
        except PermissionError:
            print(f"Permission denied to delete '{self.testProjectDir}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        return super().tearDown()
    
    def test_setVariable(self):
        self.assertFalse(self.varM.setVariable("1111var1","hello"))

        self.varM.setVariable("var1","hello")
        self.assertEqual(self.varM.Variables['var1'],'hello')

        self.varM.setVariable("VAR1","hi")
        self.assertEqual(self.varM.Variables['var1'],'hi')

    def test_saveVariables(self):
        self.varM.setVariable("var1","hello")
        self.varM.setVariable("var2","helo")
        self.varM.saveVariables()

        variablesPath = os.path.join(self.testProjectDir,"variables.json")
        with open(variablesPath, 'r') as file:
            varDict = json.load(file) 
        
        self.assertDictEqual(varDict, self.varM.Variables)
    
    def test_loadVariables(self):
        variables = {}
        variables['var1'] = 'hello'
        variables['var2'] = 'hlo'

        variablesPath = os.path.join(self.testProjectDir,"variables.json")
        with open(variablesPath, 'w') as file:
            json.dump(variables, file, indent=4)

        self.varM.loadVariables()
        self.assertDictEqual(variables, self.varM.Variables)
    
    def test_deleteVariable(self):
        self.varM.setVariable('var', 1)
        self.varM.setVariable('var1', 2)
        self.varM.setVariable('var2', 3)
        self.varM.deleteVariable('var1')

        variablesPath = os.path.join(self.testProjectDir,"variables.json")
        with open(variablesPath, 'r') as file:
            varDict = json.load(file) 

        self.assertDictEqual(varDict, {'var':1, 'var2':3})

    def test_get(self):
        self.varM.setVariable('var', 1)
        self.varM.setVariable('var1', 2)
        self.varM.setVariable('var2', 3)

        get1 = self.varM.get('asda')
        get2 = self.varM.get('VAR2')

        self.assertEqual(get1, None)
        self.assertEqual(get2, 3)


