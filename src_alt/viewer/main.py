import sys
import os
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
from SceneView import SceneView
import json

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
        self.showMessage("Options menu (not implemented)")

    def quitApp(self):
        self.close()

    def beginStory(self):
        self.centralWidget = SceneView(self.storyFilePath)
        self.setStyleSheet("background-color: #333;")
        self.setCentralWidget(self.centralWidget)

    def loadSave(self):
        #loadStory function but from a save.json file
        #self.showMessage("Loading saved game (not implemented)")
        savePath = os.path.relpath(self.storyFilePath)
        if os.path.exists(os.path.relpath(self.storyFilePath, "save.json")):
            with open(savePath, 'r') as file:
                #figure out saving linelog
                return 1

    def createSave(self):
        if (os.path.exists(self.storyFilePath) and isinstance(self.centralWidget, SceneView)):
            savePath = os.path.relpath(self.storyFilePath, "save.json")
            with open(savePath, 'w') as file:
                #add variable manager
                json.dump({"log": self.centralWidget.lineLog, "current": self.centralWidget.currentLineIndex, "variables": {}}, file)
        self.showMessage("Progress saved")

    def showMessage(self, message):
        QMessageBox.information(self, "Message", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())
