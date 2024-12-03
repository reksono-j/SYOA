import sys
from PySide6.QtGui import (
    QAccessible
)
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit, QGridLayout,
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QTimer
import json
import os
from styles import *

class UICustomizeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(500, 500)
        self.settingsDict = {}
        self.importSettings()
        self.initParameters()
        self.initUI()

    def initParameters(self):
        self.opened = False
        
        #accessibility
        self.setAccessibleName("Settings Menu")
        self.accessibilityInterface = QAccessibleWidget(self, r=QAccessible.Grouping, name="Settings Menu")

    def initUI(self):
        self.setStyleSheet(APP_STYLE_DARK)
        #menu settings
        self.setWindowTitle("Settings")

        #vertical box layout for group box
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        #inner layer for form, out layer (groupbox) for saving
        self.innerForm = QWidget(self)
        self.innerForm.layout = QFormLayout()

        #inner form accessibility
        self.innerForm.setAccessibleName("Settings Menu")
        self.innerForm.accessibilityInterface = QAccessibleWidget(self.innerForm, r=QAccessible.List, name="Settings Menu Form")


        #ui options boxes setup
        #set typeface
        self.innerForm.bgmSpinBox = QSpinBox(self)
        self.innerForm.bgmSpinBox.setAccessibleName("Background Music Volume")
        self.innerForm.bgmSpinBox.setMinimum(0)
        self.innerForm.bgmSpinBox.setMaximum(100)
        self.innerForm.bgmSpinBox.setValue(int(self.settingsDict["bgm"]))
        #self.innerForm.bgmSpinBox.activated.connect(lambda: QAccessible.updateAccessibility(QAccessibleEvent(self.innerForm.accessibilityInterface, QAccessible.Alert)))

        #set font size
        self.innerForm.sfxSpinBox = QSpinBox(self)
        self.innerForm.sfxSpinBox.setAccessibleName("Sound Effects Volume")
        self.innerForm.sfxSpinBox.setMinimum(0)
        self.innerForm.sfxSpinBox.setMaximum(100)
        self.innerForm.sfxSpinBox.setValue(int(self.settingsDict["sfx"]))

        #set font color
        self.innerForm.dialogueSpinBox = QSpinBox(self)
        self.innerForm.dialogueSpinBox.setAccessibleName("Dialogue Volume")
        self.innerForm.dialogueSpinBox.setMinimum(0)
        self.innerForm.dialogueSpinBox.setMaximum(100)
        self.innerForm.dialogueSpinBox.setValue(int(self.settingsDict["tts"]))

        #layout of form menu
        self.innerForm.layout.addRow(self.tr("Background Music Volume:"), self.innerForm.bgmSpinBox)
        self.innerForm.layout.addRow(self.tr("Sound Effects Volume:"), self.innerForm.sfxSpinBox)
        self.innerForm.layout.addRow(self.tr("Dialogue Volume:"), self.innerForm.dialogueSpinBox)
        self.innerForm.setLayout(self.innerForm.layout)

        #add form menu to group box
        self.layout.addWidget(self.innerForm)

        #create save settings button
        self.buttonSave = QPushButton("Save", self)
        self.buttonSave.setAccessibleName("Save Settings")
        self.buttonSave.clicked.connect(lambda: self.updateDict())

        #add save button to group box
        self.layout.addWidget(self.buttonSave)

        #finalize layout
        self.setLayout(self.layout)

        #prevent showing on start-up
        self.close()

    def toggleUI(self):
        if (self.opened):
            self.close()
            self.opened = False
        else:
            self.show()
            self.opened = True

    def updateDict(self):
        self.settingsDict["bgm"] = str(self.innerForm.bgmSpinBox.value())
        self.settingsDict["sfx"] = str(self.innerForm.sfxSpinBox.value())
        self.settingsDict["tts"] = str(self.innerForm.dialogueSpinBox.value())
        self.updateSettings()

    def menuToggle(self):
        self.toggleUI()

    # from keybinds.py
    def importSettings(self):
        workingDir = os.path.dirname(os.path.abspath(__file__))
        self.configPath = os.path.join(workingDir+"\\settings", 'config.json')
        with open(self.configPath, 'r') as file:
            config = json.load(file)
        self.config = config

        for key in self.config['settings']:
            self.settingsDict[key] = (self.config['settings'][key]) 

    def importVolumeDict(self):
        workingDir = os.path.dirname(os.path.abspath(__file__))
        configPath = os.path.join(workingDir+"\\settings", 'config.json')
        with open(configPath, 'r') as file:
            config = json.load(file)
        config = config

        settingsDict = {}
        for key in config['settings']:
            settingsDict[key] = (self.config['settings'][key])
        return settingsDict 


    def updateSettings(self):
        self.saveSettings()
        self.close()

    def saveSettings(self):
        for key in self.settingsDict:
            self.config['settings'][key] = self.settingsDict[key]
        
        with open(self.configPath, 'w') as file:
            json.dump(self.config, file, indent=4)
        

