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

from src_alt.editor import keybinds

class Test(unittest.TestCase):
    def setUp(self):
        # path of config file
        workingDir = os.path.dirname(os.path.abspath(__file__))
        parent_path = os.path.dirname(workingDir)
        self.configPath = os.path.join(parent_path+"\\src_alt\\editor\\settings", 'config.json')

        # creates empty file if it doesnt exist
        if not os.path.exists(self.configPath):
            with open(self.configPath, 'w') as file:
                file.write("")

        self.app = QApplication([])
        self.mainWindow = QMainWindow()
        self.manager = keybinds.ShortcutsManager(self.mainWindow)

        self.configSave = copy.deepcopy(self.manager.config)

        # make shortcuts to a known state
        configDump={}
        configDump['shortcutSettings'] = {}
        configDump['shortcutSettings']['kEy1'] = 'a'
        configDump['shortcutSettings']['kEy2'] = 'b'

        with open(self.configPath, 'w') as file:
            json.dump(configDump, file, indent=4)

        testShortcutDict = {}
        testShortcutDict['key1'] = QShortcut(QKeySequence('a'), self.mainWindow)
        testShortcutDict['key1'].name = 'kEy1'
        testShortcutDict['key2'] = QShortcut(QKeySequence('b'), self.mainWindow)
        testShortcutDict['key2'].name = 'kEy2'

        self.manager.shortcutDict = {}
        self.manager.importShortcuts()


        
        

    def tearDown(self):
        with open(self.configPath, 'w') as file:
            json.dump(self.configSave, file, indent=4)

    def test_saveShortcuts(self):
        self.manager.config['shortcutSettings']['testKey'] = 'testValue111'
        self.manager.saveShortcuts()

        with open(self.configPath, 'r') as file:
            importedConfig = json.load(file)
        
        self.assertEqual(importedConfig['shortcutSettings']['testKey'],'testValue111')

    def test_importShortcuts(self):
        configDump={}
        configDump['shortcutSettings'] = {}
        configDump['shortcutSettings']['kEy1'] = 'a'
        configDump['shortcutSettings']['kEy2'] = 'b'

        with open(self.configPath, 'w') as file:
            json.dump(configDump, file, indent=4)

        testShortcutDict = {}
        testShortcutDict['key1'] = QShortcut(QKeySequence('a'), self.mainWindow)
        testShortcutDict['key1'].name = 'kEy1'
        testShortcutDict['key2'] = QShortcut(QKeySequence('b'), self.mainWindow)
        testShortcutDict['key2'].name = 'kEy2'

        self.manager.shortcutDict = {}
        self.manager.importShortcuts()

        self.maxDiff = None
        self.assertEqual(testShortcutDict['key1'].keys().__str__(), self.manager.shortcutDict['key1'].keys().__str__())
        self.assertEqual(testShortcutDict['key2'].keys().__str__(), self.manager.shortcutDict['key2'].keys().__str__())
        self.assertEqual(testShortcutDict['key1'].name, self.manager.shortcutDict['key1'].name)
        self.assertEqual(testShortcutDict['key2'].name, self.manager.shortcutDict['key2'].name)
        self.assertEqual(len(testShortcutDict), len(self.manager.shortcutDict))

    def test_addShortcut(self):
        self.manager.addShortcut(QKeySequence('c'), 'key1', lambda:None)
        self.assertEqual(self.manager.shortcutDict['key1'].key().toString(), 'A', msg=f'imported shortcuts\' must take precedence')

        self.manager.addShortcut(QKeySequence('c'), 'key4', lambda:None)
        self.assertEqual(self.manager.shortcutDict['key4'].key().toString(), 'C')


    
    def test_shortcutsMenu(self):
        menu = keybinds.ShortcutsMenu(self.manager, self.mainWindow)

        self.assertEqual(len(menu.labelButtonPairs), 2)
        

if __name__ == "__main__":
    unittest.main()
