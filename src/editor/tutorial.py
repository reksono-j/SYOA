import sys 
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QShortcut, QKeySequence, QTextDocument
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit, QHBoxLayout, QWidget, QLayout, QTextBrowser
)
from pathlib import Path
import io
import os
from src.editor.ProjectMenu import *

class TutorialDialog(QDialog):   
    def __init__(self):
        super().__init__()
        self.tutorialFile = "userguide.md"
        self.tutorialFilePath = Path(os.path.dirname(os.path.abspath(__file__)), "userguide.md")
        self.tutorialText = ""
        self.setMinimumSize(400, 500)
        with open(self.tutorialFilePath, 'r') as file:
            self.tutorialText = file.read()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tutorial Menu")
        self.setAccessibleName("Tutorial Menu")
        self.layout = QVBoxLayout()
        self.textbox = QTextBrowser()
        self.textbox.setSource(QUrl(self.tutorialFile))
        self.layout.addWidget(self.textbox)
        self.setLayout(self.layout)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    test = TutorialDialog()
    print(test.tutorialText)
    test.exec()
    sys.exit(app.exec())