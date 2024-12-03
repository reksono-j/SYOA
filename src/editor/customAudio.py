from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QLabel,QWidget,QVBoxLayout, QComboBox, QFileDialog,  QMessageBox,
    QHBoxLayout, QListWidget, QListWidgetItem, QInputDialog, QSizePolicy
)
from PySide6.QtCore import Qt, QUrl
from src.editor.projectManager import ProjectManager
import sys, shutil, os
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class CustomAudioWidget(QWidget):
    def __init__(self, fileName:str, filePath:str, listWidget:'AudioWidgetsList', parent=None):
        super(CustomAudioWidget, self).__init__(parent)

        self.setObjectName("CustomAudioWidget")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setMinimumHeight(40)
        self.filePath = filePath
        self.listWidget = listWidget
        
        self.mediaPlayer = QMediaPlayer(self)        
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10) 
        
        self.label = QLabel(fileName)
        self.label.setAccessibleName(fileName)
        self.playButton = QPushButton("Play")
        self.playButton.setAccessibleName(f"Play {fileName}")
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setAccessibleName(f"Delete {fileName}")
        self.renameButton = QPushButton("Rename")
        self.renameButton.setAccessibleName(f"Rename {fileName}")
    
        
        for button in [self.playButton, self.deleteButton, self.renameButton]:
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) 
            button.setMinimumSize(button.sizeHint())
            button.adjustSize()
        
        self.playButton.clicked.connect(self.play)
        self.deleteButton.clicked.connect(self.delete)
        self.renameButton.clicked.connect(self.rename)
        
        layout.addWidget(self.label)
        layout.addWidget(self.playButton)
        layout.addWidget(self.renameButton)
        layout.addWidget(self.deleteButton)

        self.setLayout(layout)
        self.adjustSize()

    def delete(self):
        try:
            os.remove(self.filePath)
        except FileNotFoundError:
            print(f"{self.filePath} does not exist.")
        except PermissionError:
            print(f"Permission denied to delete {self.filePath}.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        self.listWidget.populateList()
    
    def play(self):
        url = QUrl.fromLocalFile(self.filePath)
        self.mediaPlayer.setSource(url)
        self.mediaPlayer.play()

    def rename(self):
        newName, ok = QInputDialog.getText(self, 'Renaming', 'Enter a new name:')

        if ok:
            dirPath = os.path.dirname(self.filePath)
            newFilePath = os.path.join(dirPath, newName+".mp3")
            try:
                print(newFilePath)
                os.rename(self.filePath, newFilePath)
                self.listWidget.populateList()
            except FileNotFoundError:
                print(f"Bad path, either: {self.filePath} \nOr: {newFilePath}")
            except PermissionError:
                print(f"Permission denied to rename '{self.filePath}'.")
            except Exception as e:
                print(f"An error occurred: {e}")
                
    def showEvent(self, event):
        super().showEvent(event)
        self.playButton.adjustSize()
        self.deleteButton.adjustSize()
        self.renameButton.adjustSize()
        
class AudioWidgetsList(QListWidget):
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.populateList()
    
    def setDir(self, directory):
        self.directory = directory
        self.populateList()

    def populateList(self):
        self.clear()

        if os.path.isdir(self.directory):
            for filename in os.listdir(self.directory):
                filePath = os.path.join(self.directory, filename)
                
                if filePath.lower().endswith('.mp3'):
                    audioWidget = CustomAudioWidget(filename, filePath, self) # creates the actual widget

                    # creates the list item object that is to be added to the QListWidget
                    listItem = QListWidgetItem(self)
                    listItem.setSizeHint(audioWidget.sizeHint())
                    self.addItem(listItem)
                    self.setItemWidget(listItem, audioWidget)
    
class CustomAudio():
    _currentSceneName = None
    _mainWindow = None
    _audioWidgetList = None
    _sceneDir = None
    _projectManager = None
    
    def __init__(self):
        self._projectManager = ProjectManager()
        if self._currentSceneName:
            self._audioWidgetList = AudioWidgetsList(self._currentSceneName)    
        else:
            self._audioWidgetList = AudioWidgetsList("")
        self._setupFolders()
    
    def _setupFolders(self):
        projectPath = self._projectManager.getCurrentFilePath()
        if not projectPath:
            raise ValueError("Project path not set.")
        
        audioDir = os.path.join(projectPath, "audio")
        os.makedirs(audioDir, exist_ok=True)
        os.makedirs(os.path.join(audioDir, "BGM"), exist_ok=True)
        os.makedirs(os.path.join(audioDir, "SFX"), exist_ok=True)

    def _updateSceneDir(self):
        # Get the current project path from ProjectManager
        projectPath = self._projectManager.getCurrentFilePath()
        if not projectPath:
            raise ValueError("Project path not set.")
        
        audioDir = os.path.join(projectPath, "audio")
        os.makedirs(audioDir, exist_ok=True)
        self._sceneDir = os.path.join(audioDir, self._currentSceneName)
        os.makedirs(self._sceneDir, exist_ok=True)
        

    def _getMainWindow(self):
        if self._mainWindow is None:
            print("getting mainWindow is not set up yet")
        return self._mainWindow
    
    def openFileExplorer(self):
        if self._currentSceneName is None:
            # create simple alert box when there is no scene selected
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information) 
            msg_box.setText("Please select a scene name first") 
            msg_box.setWindowTitle("Alert") 
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        else:
            sourceFilePath, _ = QFileDialog.getOpenFileName(self._mainWindow, "Open File", "", "MP3 Files (*.mp3)")

            if sourceFilePath:
                os.makedirs(self._sceneDir, exist_ok=True)
                shutil.copy(sourceFilePath, self._sceneDir)
                self._audioWidgetList.populateList()

    def renameScene(self, original:str, new:str):
        workingDir = os.path.dirname(os.path.abspath(__file__))

        originalDir = os.path.join(workingDir, "audio", original)
        newDir = os.path.join(workingDir, "audio", new)

        # make sure originalDir exists
        if os.path.isdir(originalDir):
            os.rename(originalDir, newDir)
            self._currentSceneName = new
            self._updateSceneDir()
            self.getAudioListWidget().setDir(self._sceneDir)
        else:
            print(f"Original directory does not exist: {originalDir}")
    
    def setCurrentScene(self, newSceneName:str):
        self._currentSceneName = newSceneName
        self._updateSceneDir()
        self.getAudioListWidget().setDir(self._sceneDir)

    def setProjectManager(self):
        self._projectManager = ProjectManager()
        
    def getAudioListWidget(self):
        return self._audioWidgetList

class AudioManagerDialog(QDialog):
    def __init__(self):

        self.setWindowTitle("Audio Manager")
        self.setMinimumSize(400, 300)
        self.setObjectName("AudioManager")

        mainLayout = QVBoxLayout()
        controlLayout = QHBoxLayout()
        
        self.sceneSelector = QComboBox()
        self.sceneSelector.currentTextChanged.connect(self.changeScene)
        self.projectManager = ProjectManager()
        self.customAudio = CustomAudio()
        
        self.addSceneButton = QPushButton("Add Scene")
        self.addSceneButton.clicked.connect(self.addScene)
        self.removeSceneButton = QPushButton("Remove Scene")
        self.removeSceneButton.clicked.connect(self.removeScene)
        self.addAudioButton = QPushButton("Add Audio File")
        self.addAudioButton.clicked.connect(self.customAudio.openFileExplorer)

        controlLayout.addWidget(QLabel("Scenes:"))
        controlLayout.addWidget(self.sceneSelector)
        controlLayout.addWidget(self.addSceneButton)
        controlLayout.addWidget(self.removeSceneButton)
        controlLayout.addWidget(self.addAudioButton)

        self.audioListWidget = self.customAudio.getAudioListWidget()

        mainLayout.addLayout(controlLayout)
        mainLayout.addWidget(self.audioListWidget)
        self.setLayout(mainLayout)

        self.refreshSceneList()

    def addScene(self):
        sceneName, ok = QInputDialog.getText(self, "Add Scene", "Enter scene name:")
        if ok and sceneName:
            self.customAudio.setCurrentScene(sceneName)
            self.refreshSceneList()

    def removeScene(self):
        sceneName = self.sceneSelector.currentText()
        if not sceneName:
            QMessageBox.information(self, "Remove Scene", "No scene selected.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Removal", f"Are you sure you want to remove '{sceneName}'?", 
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.customAudio.renameScene(sceneName, None)
            self.refreshSceneList()

    def changeScene(self, sceneName):
        if sceneName:
            self.customAudio.setCurrentScene(sceneName)

    def refreshSceneList(self):
        projectPath = self.projectManager.getCurrentFilePath()
        audioDir = os.path.join(projectPath, "audio")
        os.makedirs(audioDir, exist_ok=True)

        scenes = [d for d in os.listdir(audioDir) if os.path.isdir(os.path.join(audioDir, d))]
        self.sceneSelector.clear()
        self.sceneSelector.addItems(scenes)

        # Set the first scene as the default if none is selected
        if scenes:
            self.sceneSelector.setCurrentIndex(0)
            self.customAudio.setCurrentScene(scenes[0])


if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("some window")
            self.setGeometry(100, 100, 1200, 800)
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            self.currentScene = QLabel()
            self.currentScene.setText("Current scene: None")

            self.button = QPushButton("Open file explorer", self)
            self.button.clicked.connect(self.buttonFunc)

            self.textInput = QLineEdit()
            self.textInput.setPlaceholderText("Type scene name here to set scene name. Press enter")
            self.textInput.returnPressed.connect(self.textInputCallback)

            self.textInput2 = QLineEdit()
            self.textInput2.setPlaceholderText("Rename current scene name. Press enter")
            self.textInput2.returnPressed.connect(self.textInputCallback2)

            layout = QVBoxLayout()
            layout.addWidget(self.currentScene)
            layout.addWidget(self.button)
            layout.addWidget(self.textInput)
            layout.addWidget(self.textInput2)
            self.customAudio = CustomAudio()
            layout.addWidget(self.customAudio.getAudioListWidget())
            central_widget.setLayout(layout)


        def buttonFunc(self):
            self.customAudio.openFileExplorer()
        
        def textInputCallback(self):
            self.customAudio.setCurrentScene(self.textInput.text())
            self.currentScene.setText("Current scene: " + self.textInput.text())
        
        def textInputCallback2(self):
            self.customAudio.renameScene(self.customAudio._currentSceneName, self.textInput2.text())
            self.currentScene.setText("Current scene: " + self.textInput2.text())

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec())