from PySide6.QtWidgets import (
    QWidget, QMessageBox,QFrame, QSizePolicy,
    QVBoxLayout, QPushButton 
)
from PySide6.QtCore import Qt, Signal
from styles import *
import tutorial

class HomeMenu(QWidget):
    CreateProject = Signal()
    OpenExistingProject = Signal()
    ShowTutorial = Signal()
    OpenPreferences = Signal()
    ShowFaq = Signal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.optionsFrame = QFrame()
        self.optionsFrame.setObjectName("homeMenuFrame") 
        self.optionsFrame.setMinimumSize(300, 400) 

        self.optionsLayout = QVBoxLayout(self.optionsFrame)
        self.optionsLayout.setContentsMargins(0, 0, 0, 0)  

        self.startProjectButton = self.createButton("Start a new project", self.CreateProject)
        self.openProjectButton = self.createButton("Open existing project", self.OpenExistingProject)
        self.tutorialButton = self.createButton("Tutorial", self.ShowTutorial)
        self.preferencesButton = self.createButton("Preferences", self.OpenPreferences)
        self.faqButton = self.createButton("FAQ", self.ShowFaq)

        self.optionsLayout.addWidget(self.startProjectButton)
        self.optionsLayout.addWidget(self.openProjectButton)
        self.optionsLayout.addWidget(self.tutorialButton)
        self.optionsLayout.addWidget(self.preferencesButton)
        self.optionsLayout.addWidget(self.faqButton)

        self.layout.addWidget(self.optionsFrame, alignment=Qt.AlignCenter)

        self.ShowTutorial.connect(lambda: self.showTutorial)
        self.OpenPreferences.connect(lambda: self.OpenPreferences)
        self.ShowFaq.connect(lambda: self.printMessage("FAQ", "WIP: FAQ under construction")) # TODO: add FAQ

    def createButton(self, text, signal):
        button = QPushButton(text)
        button.clicked.connect(signal.emit)  
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setAccessibleName(text)
        return button

    def printMessage(self, title, text):
        QMessageBox.information(self, title, text)

    def showTutorial(self):
        self.dialog = tutorial.TutorialDialog()
        self.dialog.exec()
        

