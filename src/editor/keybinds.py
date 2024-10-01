from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt
import json
import os
import speechToText

# for opening the shortcuts changer menu
class ShortcutsMenu(QDialog):
    def __init__(self, shortcutsManager, parent):
        super(ShortcutsMenu, self).__init__(parent)
        self.setWindowTitle("Shortcuts Menu")
        self.setGeometry(parent.rect())

        self.shortcutsManager = shortcutsManager

        self.button = "" # to reference the button that was clicked

        # layout for the widgets
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        for key in shortcutsManager.shortcutDict:
            label = QLabel(shortcutsManager.shortcutDict[key].name)
            button = QPushButton(shortcutsManager.shortcutDict[key].key().toString())
            button.thisShortcut = shortcutsManager.shortcutDict[key]
            button.clicked.connect(lambda: self.initiateReplacingKeys())
            self.layout.addRow(label, button)
        
        # transparent overlay
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
        self.overlay.setGeometry(self.rect())
        self.overlay.hide() 

        # layout and widgets for the keybinding screen
        self.keybindInputWidget = QKeySequenceEdit(self)
        self.keybindInputWidget.hide()
        self.keybindInputWidget.editingFinished.connect(self.finishReplacingKeys)

    def initiateReplacingKeys(self):
        self.button = self.sender() # gets the reference to the button that was clicked
        self.showKeybindScreen()

    def finishReplacingKeys(self):
        newKeySequence = self.keybindInputWidget.keySequence()
        self.button.thisShortcut.setKey(newKeySequence)
        self.hideKeybindScreen()
        self.button.setText(self.button.thisShortcut.key().toString())
        self.shortcutsManager.saveShortcuts()

    def showKeybindScreen(self):
        self.overlay.setGeometry(self.rect())
        self.overlay.show()

        self.keybindInputWidget.setGeometry(
            (self.width() - 300) // 2,
            (self.height() - 100) // 2,
            300, 100
        )
        self.keybindInputWidget.show()  
        self.keybindInputWidget.setFocus()

    def hideKeybindScreen(self):
        self.overlay.hide()
        self.keybindInputWidget.hide()


class ShortcutsManager:
    def __init__(self, window) -> None:
        self.shortcutDict = {} # for the shortcuts menu
        self.window = window        
        self.importShortcuts()

        #self.addShortcut("ctrl+q","Quit",self.window.close)
        #self.addShortcut("/","Replace Shortcuts Menu",lambda: self.openShortcutsMenu())
        #self.addShortcut("o","Open IDE",self.window.button.click)
        #self.addShortcut("p","Open Hand Held Mode",self.window.button1.click)
        #self.addShortcut("t","Start Transcription",speechToText.STT.recordCallback)

    def addShortcut(self, keySequence, displayedName, callbackFunction):
        """
        imported shortcuts will take priority
        """
        if displayedName in self.shortcutDict: # imported shortcut from settings, so just connect the function
            self.shortcutDict[displayedName].activated.connect(callbackFunction)
        else: # did not get shortcut from settings, so create new shortcut
            shortcut = QShortcut(QKeySequence(keySequence), self.window)
            shortcut.name = displayedName
            shortcut.activated.connect(function)
            self.shortcutDict[displayedName] = shortcut

    def openShortcutsMenu(self):
        # Open the options menu
        menu = ShortcutsMenu(self, self.window)
        menu.exec_()  # This will block execution until the dialog is closed
    
    def saveShortcuts(self):
        for key in self.shortcutDict:
            self.config['shortcutSettings'][key] = self.shortcutDict[key].key().toString()
        
        with open(self.configPath, 'w') as file:
            json.dump(self.config, file, indent=4)

    def importShortcuts(self):
        # gets the path to the config file
        workingDir = os.path.dirname(os.path.abspath(__file__))
        self.configPath = os.path.join(workingDir+"\\settings", 'config.json')
        with open(self.configPath, 'r') as file:
            config = json.load(file)
        self.config = config

        for key in self.config['shortcutSettings']:
            keySequence = QKeySequence(self.config['shortcutSettings'][key])
            self.shortcutDict[key] = QShortcut(keySequence, self.window)
            self.shortcutDict[key].name = key
