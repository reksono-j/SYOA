import os, json, time, re, uuid
from src_alt.viewer.singleton import Singleton
from src_alt.viewer.loader import Loader
from pathlib import Path
import platform
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QListWidget, QPushButton, QMessageBox, QDialog,
    QLabel, QLineEdit, QScrollArea, QHBoxLayout, QSpacerItem,
    QSizePolicy
)


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
    


class SaveManagerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.fileManager = FileManager()
        if self.fileManager._loader.projectLoaded:
            self.saveDir = self.fileManager.getSaveFolderPath()
            self.createSaveDirectories()
        else:
            self.close()

        self.layout = QVBoxLayout(self)
                
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        
        # The scroll area will be where the saves exist
        self.slotContainer = QWidget()
        self.slotLayout = QVBoxLayout(self.slotContainer)
        
        self.populateSlots()

        self.slotContainer.setLayout(self.slotLayout)
        self.scrollArea.setWidget(self.slotContainer)
        self.layout.addWidget(self.scrollArea)

    def populateSlates(self): # TODO
        for i in range(16): 
            slotWidget = QWidget()
            slotLayoutRow = QHBoxLayout(slotWidget)
            slotLabel = QLabel(f"Slot {i+1} - Empty")  # TODO: Load
            slotLabel.setStyleSheet("color: white; font-size: 16px;")
            slotLayoutRow.addWidget(slotLabel)

            slotLayoutRow.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
            self.slotLayout.addWidget(slotWidget)
    
    def createSaveDirectories(self):
        if not os.path.exists(self.saveDir):
            os.mkdir(self.saveDir, parents=True)
        self.manualDir = os.path.join(self.saveDir, "manual")
        self.autosaveDir = os.path.join(self.saveDir, "autosave")
        self.quicksaveDir = os.path.join(self.saveDir, "quicksave")
        os.makedirs(self.manualDir, exist_ok=True)
        os.makedirs(self.autosaveDir, exist_ok=True)
        os.makedirs(self.quicksaveDir, exist_ok=True)

    def addSave(self, saveType, name):
        timestamp = time.time()
        saveId = uuid.uuid4().hex
        saveFileName = f"{saveType}_{int(timestamp)}_{saveId}_{name}.save"
        timestamp = time.strftime("%B %d, %Y, %I:%M %p", time.localtime(timestamp)) 
        saveMetadata = {
            "saveType": saveType,
            "timestamp": timestamp,
            "name": name,
            "saveId": saveId
        }

        metadataFile = os.path.join(self.saveDir, f"{saveFileName}.json")
        with open(metadataFile, 'w') as f:
            json.dump(saveMetadata, f)

        self.saveList.addItem(f"{saveType.capitalize()} Save: {name} at {timestamp}")

    def loadSave(self):
        selectedItem = self.saveList.currentItem()
        if selectedItem:
            saveName = selectedItem.text().split(":")[1].strip()
            saveFileName = self.getSaveFileNameByName(saveName)

            if saveFileName:
                savePath = os.path.join(self.saveDir, f"{saveFileName}.save")
                if os.path.exists(savePath):
                    # TODO: Save loading
                    #self.fileManager.readSaveFile
                    QMessageBox.information(self, "Load Save", f"Loaded save from: {savePath}")
                else:
                    QMessageBox.warning(self, "Load Save", "Save file not found!")
            else:
                QMessageBox.warning(self, "Load Save", "Save name not found.")
        else:
            QMessageBox.warning(self, "Load Save", "No save selected!")

    def getSaveFileNameByName(self, name):
        for root, dirs, files in os.walk(self.saveDir):
            for file in files:
                if name in file:
                    return file.replace('.save', '')
        return None

    def deleteSave(self):
        selectedItem = self.saveList.currentItem()
        if selectedItem:
            saveName = selectedItem.text().split(":")[1].strip()
            saveFileName = self.getSaveFileNameByName(saveName)

            if saveFileName:
                savePath = os.path.join(self.saveDir, f"{saveFileName}.save")
                metadataPath = os.path.join(self.saveDir, f"{saveFileName}.json")

                if os.path.exists(savePath):
                    os.remove(savePath)
                    os.remove(metadataPath)
                    self.saveList.takeItem(self.saveList.row(selectedItem))
                    QMessageBox.information(self, "Delete Save", "Save deleted successfully!")
                else:
                    QMessageBox.warning(self, "Delete Save", "Save file not found!")
            else:
                QMessageBox.warning(self, "Delete Save", "Save name not found.")
        else:
            QMessageBox.warning(self, "Delete Save", "No save selected!")



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
        
        # TODO: Make the save file
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
