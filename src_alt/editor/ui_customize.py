import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import json
import os

class UICustomizeMenu(QGroupBox):
    def __init__(self, UICustomizeManager, parent):
        super(UICustomizeMenu, self).__init__(parent)
        self.parent = parent
        self.UICustomizeManager = UICustomizeManager
        self.initParameters()
        self.initUI()

    def initParameters(self):
        self.opened = False
        
        #accessibility
        self.setAccessibleName("UI Settings Menu")
        self.setAccessibleDescription("Menu for changing UI")
        self.accessibilityInterface = QAccessibleWidget(self, r=QAccessible.Grouping, name="UI Settings Menu")

    def initUI(self):
        #menu settings
        self.setTitle("UI Settings")
        self.setAlignment(2)
        #self.setGeometry(0, 100, 1280, 700)

        #vertical box layout for group box
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        #inner layer for form, out layer (groupbox) for saving
        self.innerForm = QWidget(self)
        self.innerForm.layout = QFormLayout()

        #inner form accessibility
        self.innerForm.setAccessibleName("UI Settings Menu")
        self.innerForm.setAccessibleDescription("Contains UI settings controls")
        self.innerForm.accessibilityInterface = QAccessibleWidget(self.innerForm, r=QAccessible.List, name="UI Settings Menu Form")


        #ui options boxes setup
        #set typeface
        self.innerForm.fontFamilyComboBox = QFontComboBox(self)
        self.innerForm.fontFamilyComboBox.setAccessibleName("Font Family Setting")
        self.innerForm.fontFamilyComboBox.setAccessibleDescription("Change font family here")
        self.innerForm.fontFamilyComboBox.setCurrentFont(self.parent.font())
        #self.innerForm.fontFamilyComboBox.activated.connect(lambda: QAccessible.updateAccessibility(QAccessibleEvent(self.innerForm.accessibilityInterface, QAccessible.Alert)))

        #set font size
        self.innerForm.fontSizeSpinBox = QSpinBox(self)
        self.innerForm.fontSizeSpinBox.setAccessibleName("Font Size Setting")
        self.innerForm.fontSizeSpinBox.setAccessibleDescription("Change font size here")
        self.innerForm.fontSizeSpinBox.setMinimum(12)
        self.innerForm.fontSizeSpinBox.setMaximum(72)
        self.innerForm.fontSizeSpinBox.setValue(int(self.UICustomizeManager.settingsDict["Font Size"]))

        #set font color
        self.innerForm.fontColorComboBox = QComboBox(self)
        self.innerForm.fontColorComboBox.setAccessibleName("Font Color Setting")
        self.innerForm.fontColorComboBox.setAccessibleDescription("Change font color here")
        self.innerForm.fontColorComboBox.setEditText(self.UICustomizeManager.settingsDict["Font Color"])
        self.innerForm.fontColorComboBox.setEditable(False)
        self.innerForm.fontColorComboBox.addItem("black")
        self.innerForm.fontColorComboBox.addItem("white")
        self.innerForm.fontColorComboBox.addItem("red")
        self.innerForm.fontColorComboBox.addItem("blue")
        self.innerForm.fontColorComboBox.setCurrentText(self.UICustomizeManager.settingsDict["Font Color"])

        #layout of form menu
        self.innerForm.layout.addRow(self.tr("Font Family:"), self.innerForm.fontFamilyComboBox)
        self.innerForm.layout.addRow(self.tr("Font Size:"), self.innerForm.fontSizeSpinBox)
        self.innerForm.layout.addRow(self.tr("Font Color:"), self.innerForm.fontColorComboBox)
        self.innerForm.setLayout(self.innerForm.layout)

        #add form menu to group box
        self.layout.addWidget(self.innerForm)

        #create save settings button
        self.buttonSave = QPushButton("Save", self)
        self.buttonSave.setAccessibleName("Save Settings")
        self.buttonSave.setAccessibleDescription("Save UI settings here")
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
        self.UICustomizeManager.settingsDict["Font Family"] = self.innerForm.fontFamilyComboBox.currentFont().family()
        self.UICustomizeManager.settingsDict["Font Size"] = str(self.innerForm.fontSizeSpinBox.value())
        self.UICustomizeManager.settingsDict["Font Color"] = self.innerForm.fontColorComboBox.currentText()
        self.UICustomizeManager.updateSettings()

class UICustomizeManager:
    def __init__(self, window) -> None:
        self.window = window
        self.settingsDict = {}
        self.importSettings()
        self.applySettings()
        self.menu = UICustomizeMenu(self, window)

    def menuToggle(self):
        self.menu.toggleUI()

    # from keybinds.py
    def importSettings(self):
        workingDir = os.path.dirname(os.path.abspath(__file__))
        self.configPath = os.path.join(workingDir+"\\settings", 'config.json')
        with open(self.configPath, 'r') as file:
            config = json.load(file)
        self.config = config

        for key in self.config['uiSettings']:
            self.settingsDict[key] = (self.config['uiSettings'][key]) 

    def applySettings(self):
        self.window.setStyleSheet("color: " + self.settingsDict["Font Color"] + ";" +
                                  "font-size: " + self.settingsDict["Font Size"] + "pt;" +
                                  "font-family: " + self.settingsDict["Font Family"])

    def updateSettings(self):
        self.applySettings()
        self.saveSettings()

    def saveSettings(self):
        for key in self.settingsDict:
            self.config['uiSettings'][key] = self.settingsDict[key]
        
        with open(self.configPath, 'w') as file:
            json.dump(self.config, file, indent=4)
        

