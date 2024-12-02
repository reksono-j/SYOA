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

from src_alt.viewer import SceneView
from src_alt.viewer.files import FileManager
from src_alt.viewer import loader
from src_alt.viewer import variables

import logging
logging.basicConfig(level=logging.DEBUG)

class Test_Loader(unittest.TestCase):
    

    def setUp(self):
        self.workingDir = os.path.dirname(os.path.abspath(__file__))
        self.saveFilePath = os.path.join(self.workingDir, "aaaa.syoa")
        self.loader = loader.Loader()
        self.loader.setProject(self.saveFilePath)
        
        return super().setUp()
    
    def tearDown(self):
            
        return super().tearDown()

    def test_getPackagePath(self):
        self.loader.loadPackage()
        self.assertEqual(self.loader.getPackagePath(), self.saveFilePath)

    def test_getID(self):
        self.loader.loadPackage()
        self.assertEqual(self.loader.getID(), 'UFmC7DS3U8J37k8h')

    def test_getStartScene(self):
        self.loader.loadPackage()
        self.assertEqual(self.loader.getStartScene(), 'Scene1')

    def test_readSceneToDict(self):
        self.loader.loadPackage()
        self.assertDictEqual(self.loader.readSceneToDict('Scene1'), {'title': 'Scene1', 'lines': [{'type': 'dialogue', 'speaker': '', 'text': 'Hello world', 'audio': 'audio/Scene1/1.wav'}, {'type': 'choice', 'choices': [{'text': 'Hi there', 'index': 1, 'lines': [{'type': 'dialogue', 'speaker': '', 'text': 'Hi there', 'audio': 'audio/Scene1/2.wav'}]}, {'text': 'Pick up rock', 'index': 2, 'lines': [{'type': 'dialogue', 'speaker': {}, 'text': 'You picked up a rock', 'audio': 'audio/Scene1/3.wav'}, {'type': 'modify', 'action': "self.vm.set('rock', self.vm.get('rock') + 1)"}]}]}, {'comparison': "self.vm.get('rock') == 1", 'ifLines': [{'type': 'dialogue', 'speaker': '', 'text': "That's a sweet rock", 'audio': 'audio/Scene1/4.wav'}, {'type': 'dialogue', 'speaker': '', 'text': "Isn't it?", 'audio': 'audio/Scene1/5.wav'}], 'elseLines': [{'type': 'dialogue', 'speaker': {}, 'text': 'Speaker 1 looks at the ground, leans over, and picks up a rock.', 'audio': 'audio/Scene1/6.wav'}, {'type': 'dialogue', 'speaker': '', 'text': 'Wow this is an awesome rock.', 'audio': 'audio/Scene1/7.wav'}, {'type': 'dialogue', 'speaker': '', 'text': "Woah, you're right.", 'audio': 'audio/Scene1/8.wav'}], 'type': 'conditional'}, {'type': 'branch', 'next': 'Scene2'}], 'links': ['Scene2']})

    def test_loadPackage(self):
        self.loader.loadPackage()
        self.assertDictEqual(self.loader._data, {'start': 'Scene1', 'id': 'UFmC7DS3U8J37k8h'})
        self.assertDictEqual(self.loader._audioFilePaths, self.loader._audioFilePaths)
        self.assertDictEqual(self.loader._sceneFilePaths, {'Scene1': 'scripts/Scene1.json', 'Scene2': 'scripts/Scene2.json', 'Scene3': 'scripts/Scene3.json'})
        self.assertTrue(self.loader.projectLoaded)

class Test_Files(unittest.TestCase):
    def setUp(self):
        self.workingDir = os.path.dirname(os.path.abspath(__file__))
        self.saveFilePath = os.path.join(self.workingDir, "aaaa.syoa")
        self.loader = loader.Loader()
        self.loader.setProject(self.saveFilePath)
        self.loader.loadPackage()
        self.fm = FileManager()

        self.saveDirPath = Path(os.getenv('LOCALAPPDATA'))/'SYOA'/'Save'/'UFmC7DS3U8J37k8h'
        
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
    def test_getSaveFolderPath(self):
        self.assertEqual(self.fm.getSaveFolderPath(), self.saveDirPath)

    def test_createSaveFile(self):
        saveData = {"a":1,"b":2}
        self.fm.createSaveFile("b", saveData)

        with open(self.saveDirPath/'b', 'r') as file:
            readData = json.load(file)
        
        self.assertDictEqual(readData, saveData)

    def test_readSaveFile(self):
        saveData = {"a":1,"b":2}
        self.fm.createSaveFile("b", saveData)

        readData = self.fm.readSaveFile(os.path.join(self.fm.getSaveFolderPath(),"b"))
        self.assertDictEqual(saveData, readData)

class Test_Variables(unittest.TestCase):
    def setUp(self):
        self.manager = variables.ViewerVariableManager()
        
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
    def test_set_and_get_variable(self):
        self.manager.set("TestVar", "TestValue")
        self.assertEqual(self.manager.get("TestVar"), "TestValue")

    def test_case_insensitive_variables(self):
        self.manager.set("TestVar", "Value1")
        self.assertEqual(self.manager.get("testvar"), "Value1")

    def test_list_variables(self):
        self.manager.set("Var1", "Value1")
        self.manager.set("Var2", "Value2")
        variables = dict(self.manager.listVariables())
        self.assertIn("var1", variables)
        self.assertIn("var2", variables)
        self.assertEqual(variables["var1"], "Value1")
        self.assertEqual(variables["var2"], "Value2")

    def test_is_valid_name(self):
        self.assertTrue(self.manager.isValidName("ValidName"))
        self.assertFalse(self.manager.isValidName("1InvalidName"))
        self.assertFalse(self.manager.isValidName("Invalid-Name"))

    def test_load_from_dict(self):
        data = {"var1": "value1", "var2": "value2"}
        self.manager.loadFromDict(data)
        self.assertEqual(self.manager.get("var1"), "value1")
        self.assertEqual(self.manager.get("var2"), "value2")

    def test_load_initial_variables(self):
        temp_file = "test_variables.json"
        data = {"var1": "value1", "var2": "value2"}
        with open(temp_file, 'w') as file:
            json.dump(data, file)

        with open(temp_file, 'r') as file:
            self.manager.loadInitialVariables(file)

        os.remove(temp_file)

        self.assertEqual(self.manager.get("var1"), "value1")
        self.assertEqual(self.manager.get("var2"), "value2")




