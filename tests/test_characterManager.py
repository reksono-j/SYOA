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
import json
import shutil


from src_alt.editor.characterManager import Character, CharacterManager
from src_alt.editor.projectManager import ProjectManager


class Test(unittest.TestCase):
    def setUp(self):
        workingDir = os.path.dirname(os.path.abspath(__file__))
        parent_path = os.path.dirname(workingDir)
        self.projectM = ProjectManager(parent_path)
        self.projectM.createProject("testProject")
        self.testProjectDir = os.path.join(parent_path, "testProject")
        self.charM = CharacterManager()

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
    

    def test_character(self):
        c1 = Character("Don")

        self.assertEqual(c1.getName(), 'Don')
        self.assertDictEqual(c1.getAliases(), {'Don':None})

        c1.addAlias('Don1')
        self.assertDictEqual(c1.getAliases(), {'Don':None, 'Don1':None})

        c1.removeAlias('Don')
        self.assertDictEqual(c1.getAliases(), {'Don':None, 'Don1':None})
        c1.removeAlias('Don1')
        self.assertDictEqual(c1.getAliases(), {'Don':None})

        c1.renameCharacter("newDon")
        self.assertEqual(c1.getName(), 'newDon')
        self.assertDictEqual(c1.getAliases(), {'newDon':None})
    
    def test_saveCharacters(self):
        c1 = Character("Don")
        self.charM.addCharacter(c1)
        self.charM.saveCharacters()

        charsPath = os.path.join(self.testProjectDir,"characters.json")
        with open(charsPath, 'r') as file:
            charDict = json.load(file) 

        self.assertDictEqual(charDict, {'Don':{'Don':None}})
    
    def test_loadCharacters(self):
        charDict = {'Don':{'Don':None}}

        charsPath = os.path.join(self.testProjectDir,"characters.json")
        with open(charsPath, 'w') as file:
            json.dump(charDict, file, indent=4)

        self.charM.loadCharacters()

        for key in self.charM.getCharacters():
            self.assertDictEqual(charDict[key], self.charM.getCharacters()[key].aliases)
        
    def test_removeCharacter(self):
        c1 = Character("Don")
        self.charM.addCharacter(c1)
        self.charM.removeCharacter('Don')

        self.assertDictEqual({},self.charM.getCharacters())
    
    def test_updateCharacter(self):
        c1 = Character("Don")
        self.charM.addCharacter(c1)

        c1.renameCharacter("newDon")
        self.charM.updateCharacter('Don', c1)

        self.assertTrue('newDon' in self.charM.getCharacters())
        self.assertDictEqual({'newDon':None},self.charM.getCharacters()['newDon'].aliases)
        
