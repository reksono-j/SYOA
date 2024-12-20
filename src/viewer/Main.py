import sys
import os

script_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QLabel,
)
from PySide6.QtCore import Qt
from src.viewer.SceneView import SceneView
from src.viewer.files import FileManager
from options import *

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Story App")
        self.setGeometry(100, 100, 1280, 720)
        self.setMinimumSize(1024, 768)
        self.setFixedSize(1280, 720)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.setStyleSheet("background-color: #333; color: white; font-size: 16px;")

        self.titleLabel = QLabel("Welcome to the Story App")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.titleLabel)

        buttonStyle = "background-color: #007BFF; color: white; padding: 10px; border-radius: 5px;"
        disabledButtonStyle = "background-color: #555; color: #999; padding: 10px; border-radius: 5px;"
        quitButtonStyle = "background-color: #FF4D4D; color: white; padding: 10px; border-radius: 5px;"

        self.beginStoryButton = QPushButton("Begin Story")
        self.beginStoryButton.setStyleSheet(disabledButtonStyle)
        self.beginStoryButton.clicked.connect(self.beginStory)
        self.beginStoryButton.setEnabled(False)
        self.beginStoryButton.setToolTip("Start the loaded story (not accessible until a story is loaded)")
        self.layout.addWidget(self.beginStoryButton)

        self.loadSaveButton = QPushButton("Load Save")
        self.loadSaveButton.setStyleSheet(disabledButtonStyle)
        self.loadSaveButton.clicked.connect(self.loadSave)
        self.loadSaveButton.setEnabled(False)
        self.loadSaveButton.setToolTip("Load a previously saved game (not accessible until a story is loaded)")
        self.layout.addWidget(self.loadSaveButton)

        self.loadStoryButton = QPushButton("Load Story")
        self.loadStoryButton.setStyleSheet(buttonStyle)
        self.loadStoryButton.clicked.connect(self.loadStory)
        self.loadStoryButton.setToolTip("Click to load a story file")
        self.layout.addWidget(self.loadStoryButton)

        self.optionsButton = QPushButton("Options")
        self.optionsButton.setStyleSheet(buttonStyle)
        self.optionsButton.clicked.connect(self.showOptions)
        self.optionsButton.setToolTip("Open options menu")
        self.layout.addWidget(self.optionsButton)

        self.quitButton = QPushButton("Quit")
        self.quitButton.setStyleSheet(quitButtonStyle)
        self.quitButton.clicked.connect(self.quitApp)
        self.quitButton.setToolTip("Exit the application")
        self.layout.addWidget(self.quitButton)

    def updateButtonStyles(self):
        if self.beginStoryButton.isEnabled():
            self.beginStoryButton.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border-radius: 5px;")
        else:
            self.beginStoryButton.setStyleSheet("background-color: #555; color: #999; padding: 10px; border-radius: 5px;")

        if self.loadSaveButton.isEnabled():
            self.loadSaveButton.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border-radius: 5px;")
        else:
            self.loadSaveButton.setStyleSheet("background-color: #555; color: #999; padding: 10px; border-radius: 5px;")

    def loadStory(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Story File", "", "Story Files (*.syoa)", options=options)
        if fileName:
            currentDirectory = os.getcwd()
            self.storyFilePath = os.path.relpath(fileName, currentDirectory)
            self.showMessage(f"Loaded story from: {fileName}")
            self.beginStoryButton.setEnabled(True)
            self.loadSaveButton.setEnabled(True)
            self.updateButtonStyles()

    def showOptions(self):
        optionsMenu = UICustomizeDialog()
        optionsMenu.exec()

    def quitApp(self):
        self.close()

    def beginStory(self):
        self.centralWidget = SceneView(self.storyFilePath, True)
        self.setStyleSheet("background-color: #333;")
        self.setCentralWidget(self.centralWidget)

    def loadSave(self):
        files = FileManager()
        savefolder = str(files.getFilepath()/'Save')
        filepath = QFileDialog.getOpenFileName(self, "Select a File", savefolder)[0]
        try:
            scene = SceneView(self.storyFilePath, False)
            scene.loadGame(filepath)
            self.centralWidget = scene
            self.setStyleSheet("background-color: #333;")
            self.setCentralWidget(self.centralWidget)
        except Exception as e:
            print(f"There was an error loading save file: {e}")
            
        
    def showMessage(self, message):
        QMessageBox.information(self, "Message", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())
