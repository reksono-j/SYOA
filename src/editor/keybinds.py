from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt

# for opening the shortcuts changer menu
class ShortcutsMenu(QDialog):
    def __init__(self, shortcutsManager, parent):
        super(ShortcutsMenu, self).__init__(parent)
        self.setWindowTitle("Shortcuts Menu")
        self.setGeometry(parent.rect())

        self.button = "" # to reference the button that was clicked

        # layout for the widgets
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # adds the labels and buttons
        for i in range(len(shortcutsManager.shortcutList)):
            label = QLabel(shortcutsManager.shortcutList[i].name)
            button = QPushButton(shortcutsManager.shortcutList[i].key().toString())
            button.thisShortcut = shortcutsManager.shortcutList[i]
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
        print(self.button.text())
        self.showKeybindScreen()

    def finishReplacingKeys(self):
        newKeySequence = self.keybindInputWidget.keySequence()
        self.button.thisShortcut.setKey(newKeySequence)
        self.hideKeybindScreen()
        self.button.setText(self.button.thisShortcut.key().toString())

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
        self.shortcutList = [] # for the shortcuts menu
        self.window = window

    def addShortcut(self, key, name, function):
        shortcut = QShortcut(QKeySequence(key), self.window)
        shortcut.name = name
        shortcut.activated.connect(function)
        self.shortcutList.append(shortcut)

    def openShortcutsMenu(self):
        # Open the options menu
        menu = ShortcutsMenu(self, self.window)
        menu.exec_()  # This will block execution until the dialog is closed
        

