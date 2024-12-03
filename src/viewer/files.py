import os, json, time, re, uuid
from src.viewer.singleton import Singleton
from src.viewer.loader import Loader
from pathlib import Path
import platform
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QListWidget, QPushButton, QMessageBox, QDialog,
    QLabel, QLineEdit, QScrollArea, QHBoxLayout, QSpacerItem,
    QSizePolicy
)
from enum import Enum

class FileManager(metaclass=Singleton):
    def __init__(self):
        if platform.system() == 'Windows':
            self.dataFolder = Path(os.getenv('LOCALAPPDATA'))/'SYOA'
        elif platform.system() == 'Darwin':  # macOS
            self.dataFolder = Path.home()/'Library'/'Application Support'/'SYOA'
        else: # Linux
            self.dataFolder = Path.home()/'.config'/'SYOA'
    
        if not self.dataFolder.exists():
            self.createDataFolder()
        
        self._loader = Loader()
        
    def createDataFolder(self,):
        if not self.dataFolder.exists():
            try:
                self.dataFolder.mkdir(parents=True, exist_ok=False)
                saveDataFolder = self.dataFolder/'Save'
                saveDataFolder.mkdir(parents=True, exist_ok=False)
            except Exception as e:
                print(f"Failed to create folder: {e}")
        else:
            print(f"User data folder already exists: {self.dataFolder}")

    def createSaveFile(self, savename: str, data: dict):
        if self._loader.projectLoaded:
            saveDataFolder = self.dataFolder/'Save'
            try:
                if not saveDataFolder.exists():
                    saveDataFolder.mkdir(parents=True, exist_ok=False)
            except Exception as e:
                print(f"Failed to create folder: {e}")

            projectSaveFolder = saveDataFolder / self._loader.getID()
            try:
                if not projectSaveFolder.exists():
                    projectSaveFolder.mkdir(parents=True, exist_ok=False)
            except Exception as e:
                print(f"Failed to create folder: {e}")
                
            filepath = projectSaveFolder / savename
            try:
                with open(filepath, 'w') as file:
                    json.dump(data, file)
            except Exception as e:
                print(f"Failed to write save file: {e}")
        else:
            print("Failed to create save file: Project not loaded")
    
    def getSaveFolderPath(self):
        return self.dataFolder/'Save'/self._loader.getID()
    
    def readSaveFile(self, filepath:str) -> dict:
        data = None
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f"Failed to read save file: {e}")
        return data
        
    def getFilepath(self):
        return self.dataFolder

# PQ: I wrote the save system so that if we want to add quick saves, it should be easy to do.
class SaveType(Enum):
    MANUAL = 1
    QUICK  = 2
    AUTO   = 3

class SaveManager():
    def __init__(self):
        self.fileManager = FileManager()
        
    def saveGame(self, saveType: SaveType, name: str, data: dict, slotNumber: int = 0):
        timestamp = time.time()
        existingFilePath = self.getExistingFilePath(saveType, slotNumber)
        saveFileName = f"slot{slotNumber}_{saveType.name}_{int(timestamp)}_{name}.save"
        try:
            self.fileManager.createSaveFile(saveFileName, data)
        except Exception as e:
            raise e
        if existingFilePath:
            os.remove(existingFilePath)
            
    
    def getExistingFilePath(self, saveType: SaveType, slotNumber: int = 0):
        saveFolder = Path(self.fileManager.getSaveFolderPath())
        if not saveFolder.exists():
            saveFolder.mkdir()
        for file in saveFolder.iterdir():
            if file.is_file():
                if file.name.startswith(f"slot{slotNumber}_{saveType.name}"):
                    savePath = file
                    return savePath
        return ""
    
    def loadGame(self, name: str):
        path = self.fileManager.getSaveFolderPath()/name
        return self.fileManager.readSaveFile(path)
    

class SaveManagerGUI(QWidget):
    def __init__(self, saveMode: bool, callback, menuToggleCallback, parent=None):
        super().__init__(parent)
        self.saveManager = SaveManager()
        self.saveMode = saveMode
        if saveMode:
            self.getSaveDataCallback = callback
        else:
            self.loadSaveFileCallback = callback
        self.toggleMenu = menuToggleCallback
        
        self.layout = QVBoxLayout(self)
        
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet("""
        QPushButton {
            background-color: #3498db;
            color: #FFFFFF;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #474747;
        }
        QPushButton:pressed {
            background-color: #757575;
        }""")
        self.backButton.clicked.connect(self.parent().switchToPauseMenu)
        self.layout.addWidget(self.backButton)
        
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        # The scroll area will be where the saves exist
        self.slotContainer = QWidget()
        self.slotLayout = QVBoxLayout(self.slotContainer)
        
        self.populateSlots()

        self.slotContainer.setLayout(self.slotLayout)
        self.scrollArea.setWidget(self.slotContainer)
        self.layout.addWidget(self.scrollArea)

        
    def populateSlots(self):
        while self.slotLayout.count():
            item = self.slotLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            
        saveDir = self.saveManager.fileManager.getSaveFolderPath()
        saveFiles = None
        if (os.path.exists(saveDir)):
            saveFiles = os.listdir(str(saveDir))
        self.metadataArray = [dict() for _ in range(18)] 
        
        if saveFiles is not None:
            for saveFile in saveFiles:
                metadata = self.parseFileName(saveFile)
                if metadata:
                    match metadata['saveType']:
                        case 'MANUAL':
                            self.metadataArray[metadata['slotNumber']] = metadata
                        # case 'AUTO':
                        #     self.metadataArray[0] = metadata
                        # case 'QUICK':
                        #     self.metadataArray[17] = metadata

        for i in range(18):
            slotWidget = QWidget()
            slotWidget.setStyleSheet("""
            QWidget {
                background-color: #444;
                border: 2px solid #3498db;
                margin: 5px;
                padding: 10px;
                border-radius: 8px;
            }
            QWidget:hover {
                background-color: #555;
                border: 2px solid #2980b9;
            }
            QWidget:focus {
                background-color: #555;
                border: 2px solid #1f618d;
            }
            """)
            slotWidget.setFocusPolicy(Qt.StrongFocus) 
            slotLayoutRow = QHBoxLayout(slotWidget)

            metadata = self.metadataArray[i]
            if metadata:
                slotName = f"Slot {i}: {metadata['name']} ({metadata['readableTimestamp']})"
            else:
                slotName = f"Slot {i}: Empty"
            slotLabel = QLabel(slotName)
            slotLabel.setStyleSheet("color: white; font-size: 16px;")
            slotLayoutRow.addWidget(slotLabel)
            slotLayoutRow.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
            
            # Assign interaction based on saveMode
            slotWidget.mousePressEvent = lambda _, i=i: self.onSlotSelected(i)
            slotWidget.keyPressEvent = lambda e, i=i: self.onSlotKeyPress(e, i)
            self.slotLayout.addWidget(slotWidget)
    
    def parseFileName(self, fileName):
        try:
            slot, saveType, timestamp, name = fileName.split('_')
            return {
                "slotNumber": int(slot[4:]),
                "saveType": saveType,
                "readableTimestamp": time.strftime(
                    "%B %d, %Y, %I:%M %p", time.localtime(int(timestamp))
                ),
                "timestamp": timestamp,
                "name": name.rsplit('.', 1)[0],
                "filename": fileName
            }
        except ValueError:  # TODO: Handle invalid file name formats
            return None  

    def onSlotSelected(self, slotIndex):
        if self.saveMode:
            saveData = self.getSaveDataCallback()
            self.openSaveDialog(slotIndex, saveData)
            self.populateSlots()
        else:
            metadata = self.metadataArray[slotIndex]
            if metadata:
                self.loadSaveFileCallback(self.saveManager.getExistingFilePath(SaveType.MANUAL, slotIndex))
                self.toggleMenu()
            else:
                QMessageBox.information(
                    None, 
                    "Load Error", 
                    "No save data exists for this slot."
                )

    def onSlotKeyPress(self, event, slotIndex):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.onSlotSelected(slotIndex)

    def openSaveDialog(self, slotNumber, data):
        dialog = SaveCreationDialog()
        if dialog.exec():
            saveName = dialog.saveNameInput.text().strip()
            self.saveManager.saveGame(
                SaveType.MANUAL, saveName, data, slotNumber
            )
            self.populateSlots()

    # I want the UI to refresh every time you open the GUI
    def showEvent(self, event):
        super().showEvent(event)
        self.populateSlots()


class SaveCreationDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Save progress")
        self.setModal(True)
        mainLayout = QVBoxLayout()

        self.saveNameLabel = QLabel("Enter Save Name:")
        self.saveNameInput = QLineEdit()
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveGame)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)

        mainLayout.addWidget(self.saveNameLabel)
        mainLayout.addWidget(self.saveNameInput)
        mainLayout.addWidget(self.saveButton)
        mainLayout.addWidget(self.cancelButton)
        self.setLayout(mainLayout)

    def saveGame(self):
        saveName = self.saveNameInput.text().strip()
        if not saveName:
            QMessageBox.warning(self, "Save Error", "Please enter a valid save name.")
            return
        if not re.match(r'^[A-Za-z0-9_]+$', saveName):
            QMessageBox.warning(self, "Save Error", "Save name can only contain letters, numbers, and underscores.")
            return
        QMessageBox.information(self, "Save Created", f"Save '{saveName}' created.")
        self.accept()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    
    #dialog = SaveCreationDialog()
    #dialog.exec()
    
    window = SaveManagerGUI()
    window.show()
    app.exec()
