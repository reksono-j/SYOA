from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox, QFileDialog, QHBoxLayout,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit, QGridLayout, QListWidget, QListWidgetItem,
    QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt
import sys
import shutil
import os
from audioPlayer import AudioPlayer

class CustomAudioWidget(QWidget):
    def __init__(self, fileName:str, filePath:str, listWidget:'AudioWidgetsList', parent=None):
        super(CustomAudioWidget, self).__init__(parent)

        self.filePath = filePath
        self.listWidget = listWidget
        
        layout = QHBoxLayout()
        self.label = QLabel(fileName)
        self.playButton = QPushButton("Play")
        self.deleteButton = QPushButton("Delete")
        self.renameButton = QPushButton("Rename")

        self.playButton.clicked.connect(self.play)
        self.deleteButton.clicked.connect(self.delete)
        self.renameButton.clicked.connect(self.rename)
        
        layout.addWidget(self.label)
        layout.addWidget(self.playButton)
        layout.addWidget(self.renameButton)
        layout.addWidget(self.deleteButton)
        
        self.setLayout(layout)

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
        AudioPlayer.playMP3(self.filePath)

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

        else:
            print(f"Directory does not exist: {self.directory}")
    
class CustomAudio():
    _currentSceneName = None
    _mainWindow = None
    _audioWidgetList = None
    _sceneDir = None

    @staticmethod
    def _updateSceneDir():
        workingDir = os.path.dirname(os.path.abspath(__file__))
        CustomAudio._sceneDir = os.path.join(workingDir, "audio", CustomAudio._currentSceneName)

    @staticmethod
    def _getMainWindow():
        if CustomAudio._mainWindow is None:
            print("getting mainWindow is not set up yet")

        return CustomAudio._mainWindow
    
    @staticmethod
    def openFileExplorer():
        if CustomAudio._currentSceneName is None:
            # create simple alert box when there is no scene selected
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information) 
            msg_box.setText("Please select a scene name first") 
            msg_box.setWindowTitle("Alert") 
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        else:
            sourceFilePath, _ = QFileDialog.getOpenFileName(CustomAudio._mainWindow, "Open File", "", "MP3 Files (*.mp3)")

            if sourceFilePath:
                os.makedirs(CustomAudio._sceneDir, exist_ok=True)
                shutil.copy(sourceFilePath, CustomAudio._sceneDir)
                CustomAudio._audioWidgetList.populateList()

    
    @staticmethod
    def renameScene(original:str, new:str):
        workingDir = os.path.dirname(os.path.abspath(__file__))

        originalDir = os.path.join(workingDir, "audio", original)
        newDir = os.path.join(workingDir, "audio", new)

        # make sure originalDir exists
        if os.path.isdir(originalDir):
            os.rename(originalDir, newDir)
            CustomAudio._currentSceneName = new
            CustomAudio._updateSceneDir()
            CustomAudio.getAudioListWidget().setDir(CustomAudio._sceneDir)
        else:
            print(f"Original directory does not exist: {originalDir}")
    
    @staticmethod
    def setCurrentScene(newSceneName:str):
        CustomAudio._currentSceneName = newSceneName
        CustomAudio._updateSceneDir()
        CustomAudio.getAudioListWidget().setDir(CustomAudio._sceneDir)

    @staticmethod
    def getAudioListWidget():
        if CustomAudio._audioWidgetList is None:
            CustomAudio._audioWidgetList = AudioWidgetsList("")
        return CustomAudio._audioWidgetList

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

            self.button = QPushButton("open file explorer", self)
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
            layout.addWidget(CustomAudio.getAudioListWidget())
            central_widget.setLayout(layout)


        def buttonFunc(self):
            CustomAudio.openFileExplorer()
        
        def textInputCallback(self):
            CustomAudio.setCurrentScene(self.textInput.text())
            self.currentScene.setText("Current scene: " + self.textInput.text())
        
        def textInputCallback2(self):
            CustomAudio.renameScene(CustomAudio._currentSceneName, self.textInput2.text())
            self.currentScene.setText("Current scene: " + self.textInput2.text())

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec())