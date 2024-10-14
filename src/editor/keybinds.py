from PySide6.QtGui import *
#from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import json
import sys
import os

# for opening the shortcuts changer menu
class ShortcutsMenu(QDialog):
    def __init__(self, shortcutsManager, parent):
        super(ShortcutsMenu, self).__init__(parent)
        self.setWindowTitle("Shortcuts Menu")
        self.setGeometry(parent.rect())

        self.shortcutsManager = shortcutsManager

        self.button = "" # to reference the button that was clicked

        # establish accessibility interface for menu
        #self.setAccessibleName("Shortcuts Menu")
        self.setAccessibleDescription("Change shortcut keybinds here")
        #self.accessibilityInterface = QAccessibleWidget(self, role=QAccessible.Dialog, name="Shortcuts Menu")

        # layout for the widgets
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        for key in shortcutsManager.shortcutDict:
            label = QLabel(shortcutsManager.shortcutDict[key].name)
            button = QPushButton(shortcutsManager.shortcutDict[key].key().toString())
            button.thisShortcut = shortcutsManager.shortcutDict[key]
            button.clicked.connect(lambda: self.initiateReplacingKeys())
            self.layout.addRow(label, button)

            # accessibility
            #button.setAccessibleName(shortcutsManager.shortcutDict[key].name)
            button.setAccessibleDescription("Change " + shortcutsManager.shortcutDict[key].name + " keybind here")
            #button.accessibilityInterface = QAccessibleWidget(button, role=QAccessible.Button, name=shortcutsManager.shortcutDict[key].name)
        
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

        # accessibility 
        #QAccessible.updateAccessibility(QAccessibleEvent(self.accessibilityInterface, QAccessible.PopupMenuStart))
        #QAccessible.updateAccessibility(QAccessibleEvent(self.accessibilityInterface, QAccessible.Focus))

    def hideKeybindScreen(self):
        self.overlay.hide()
        self.keybindInputWidget.hide()

        # accessibility 
        #QAccessible.updateAccessibility(QAccessibleEvent(self.accessibilityInterface, QAccessible.PopupMenuEnd))
        #QAccessible.updateAccessibility(QAccessibleEvent(self.accessibilityInterface, QAccessible.Focus))


class ShortcutsManager:
    _instance = None

    def __new__(cls, _):
        if cls._instance is None:
            cls._instance = super(ShortcutsManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            print("ShortcutsManager is not defined yet.")
            return None
        else:
            return cls._instance

    def __init__(self, window) -> None:
        self.shortcutDict = {} # for the shortcuts menu
        self.window = window        
        self.importShortcuts()

    def addShortcut(self, keySequence, displayedName, callbackFunction):
        """
        imported shortcuts will take priority
        """

        dictKey = displayedName.lower()

        if dictKey in self.shortcutDict: # imported shortcut from settings, so just connect the function
            self.shortcutDict[dictKey].activated.connect(callbackFunction)
            self.shortcutDict[dictKey].name = displayedName
        else: # did not get shortcut from settings, so create new shortcut
            shortcut = QShortcut(QKeySequence(keySequence), self.window)
            shortcut.name = displayedName
            shortcut.activated.connect(callbackFunction)
            self.shortcutDict[dictKey] = shortcut

    def openShortcutsMenu(self):
        # Open the options menu
        menu = ShortcutsMenu(self, self.window)
        #QAccessible.updateAccessibility(QAccessibleEvent(menu.accessibilityInterface, QAccessible.DialogStart))
        menu.exec_()  # This will block execution until the dialog is closed
        #QAccessible.updateAccessibility(QAccessibleEvent(menu.accessibilityInterface, QAccessible.DialogEnd))
    
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    mainWindow = QMainWindow()
    textbox = ShortcutsMenu(ShortcutsManager(mainWindow),mainWindow)
    textbox.resize(1000, 500)
    textbox.show()
    sys.exit(app.exec())