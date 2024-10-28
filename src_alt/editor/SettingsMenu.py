from PySide6.QtWidgets import (
    QWidget, QMessageBox, QFrame, QPushButton, 
    QSpacerItem, QSizePolicy, QGridLayout,
)
from PySide6.QtCore import Signal
from styles import *

class SettingsMenu(QWidget):
    changeThemeSignal = Signal()
    resetPreferencesSignal = Signal()

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.optionsFrame = QFrame()
        self.optionsFrame.setMinimumSize(300, 200)  
        self.optionsFrame.setStyleSheet("background-color: #cfe5ff; border-radius: 10px;")  
        self.optionsFrame.setLineWidth(2)

        self.optionsLayout = QGridLayout(self.optionsFrame)
        self.optionsLayout.setContentsMargins(0, 0, 0, 0)  

        self.changeThemeButton = self.createButton("Change Theme", self.changeThemeSignal)
        self.resetPreferencesButton = self.createButton("Reset Preferences", self.resetPreferencesSignal)

        self.optionsLayout.addWidget(self.changeThemeButton, 0, 0)
        self.optionsLayout.addWidget(self.resetPreferencesButton, 1, 0)

        for i in range(2):  
            self.optionsLayout.setRowStretch(i, 1)

        verticalSpacerTop = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        verticalSpacerBottom = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout.addItem(verticalSpacerTop, 0, 1)  
        self.layout.addWidget(self.optionsFrame, 1, 1)  
        self.layout.addItem(verticalSpacerBottom, 2, 1)  

        self.changeThemeSignal.connect(lambda: self.printMessage("Change Theme", "Changing theme..."))
        self.resetPreferencesSignal.connect(lambda: self.printMessage("Reset Preferences", "Resetting preferences..."))

    def createButton(self, text, signal):
        button = QPushButton(text)
        button.setStyleSheet(BUTTON_STYLE)
        button.clicked.connect(signal.emit)  
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return button
        
    def printMessage(self, title, text):
        QMessageBox.information(self, title, text)