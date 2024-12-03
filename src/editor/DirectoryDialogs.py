import os
from PySide6.QtWidgets import (
    QDialog, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QMessageBox, QListWidget, QPushButton,
    QLineEdit, QLabel, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class ProjectFolderSelectDialog(QDialog):
    def __init__(self, baseDirectory):
        super().__init__()
        self.setWindowTitle("Select a Folder")
        self.setAccessibleName("Folder Selection")
        self.setModal(True)

        self.layout = QVBoxLayout(self)

        self.folderList = QListWidget()
        self.folderList.setAccessibleName("Folder List")
        self.layout.addWidget(self.folderList)

        self.selectButton = QPushButton("Select")
        self.selectButton.setAccessibleName("Select")
        self.selectButton.clicked.connect(self.selectFolder)
        self.layout.addWidget(self.selectButton)

        self.loadFolders(baseDirectory)

    def loadFolders(self, baseDirectory):
        try:
            folders = [f for f in os.listdir(baseDirectory) if os.path.isdir(os.path.join(baseDirectory, f))]
            self.folderList.addItems(folders)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load folders: {str(e)}")

    def selectFolder(self):
        selectedItems = self.folderList.selectedItems()
        if selectedItems:
            selectedFolder = selectedItems[0].text()
            self.accept()
            self.selectedFolder = selectedFolder
        else:
            QMessageBox.warning(self, "Warning", "Please select a folder.")

    def getSelectedFolder(self):
        return getattr(self, 'selectedFolder', None)


class OpenFileWidget(QTreeWidget):
    def __init__(self, folderPath, closeDialogCallback):
        super().__init__()
        self.setHeaderLabel("Files")
        self.folderPath = folderPath
        self.populateTree() 
        self.closeDialogCallback = closeDialogCallback 
        self.itemDoubleClicked.connect(self.handleItemDoubleClick)

    def populateTree(self):
        for item in os.listdir(self.folderPath):
            itemPath = os.path.join(self.folderPath, item)
            if os.path.isfile(itemPath) and item.endswith('.txt'):
                self.addFileItem(item)

    def addFileItem(self, fileName):
        fileNameWithoutExtension = os.path.splitext(fileName)[0] 
        QTreeWidgetItem(self, [fileNameWithoutExtension]) 

    def handleItemDoubleClick(self, item):
        self.performAction(item.text(0))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            currentItem = self.currentItem()
            if currentItem is not None:
                self.performAction(currentItem.text(0)) 
        else:
            super().keyPressEvent(event) 

    def performAction(self, fileName):
        print(f"Action executed for file: {fileName}")
        self.closeDialogCallback() 

class OpenFileDialog(QDialog):
    def __init__(self, folderPath):
        super().__init__()
        self.setWindowTitle("Open File Menu")
        self.setModal(True) 
        self.setWindowModality(Qt.ApplicationModal) 
        layout = QVBoxLayout(self)
        self.fileTreeWidget = OpenFileWidget(folderPath, self.close)
        layout.addWidget(self.fileTreeWidget)


class PickFilepathDialog(QDialog):
    def __init__(self, projectPath: str):
        super().__init__()
        self.setWindowTitle("Create New File")
        self.projectPath = projectPath
        self.startingScene = ""
        
        self.layout = QVBoxLayout(self)

        self.fileNameInput = QLineEdit(self)
        self.fileNameInput.setPlaceholderText("Enter filename")
        self.fileNameInput.setAccessibleName("Filename Field")
        self.layout.addWidget(QLabel("Filename:"))
        self.layout.addWidget(self.fileNameInput)

        self.directoryButton = QPushButton("Select Directory", self)
        self.directoryButton.setAccessibleName("Select Directory")
        self.layout.addWidget(self.directoryButton)

        self.selectedDirectoryLabel = QLabel("No directory selected", self)
        self.selectedDirectoryLabel.setFocusPolicy(Qt.StrongFocus)
        self.selectedDirectoryLabel.setAccessibleName(self.selectedDirectoryLabel.text())
        self.layout.addWidget(self.selectedDirectoryLabel)
        
        self.startingSceneButton = QPushButton("Select Starting Scene", self)
        self.startingSceneButton.setAccessibleName("Select Starting Scene")
        self.layout.addWidget(self.startingSceneButton)
        
        self.startingSceneLabel = QLabel("No starting scene selected", self)
        self.startingSceneLabel.setAccessibleName(self.startingSceneLabel.text())
        self.startingSceneLabel.setFocusPolicy(Qt.StrongFocus)
        self.layout.addWidget(self.startingSceneLabel)
        
        self.okButton = QPushButton("OK", self)
        self.okButton.setAccessibleName("Confirm")
        self.layout.addWidget(self.okButton)

        self.directoryButton.clicked.connect(self.openDirectoryDialog)
        self.startingSceneButton.clicked.connect(self.openStartSceneDialog)
        self.okButton.clicked.connect(self.accept)

        self.setTabOrder(self.fileNameInput, self.directoryButton)
        self.setTabOrder(self.directoryButton, self.selectedDirectoryLabel)
        self.setTabOrder(self.selectedDirectoryLabel, self.startingSceneButton)
        self.setTabOrder(self.startingSceneButton, self.startingSceneLabel)
        self.setTabOrder(self.startingSceneLabel, self.okButton)
        self.setTabOrder(self.okButton, self.fileNameInput)
    
    def openStartSceneDialog(self):
        scene = QFileDialog.getOpenFileName(self, "Select Starting Scene", self.projectPath, filter="*.txt")
        if scene:
            scene = os.path.splitext(os.path.basename(scene[0]))[0]
            self.startingSceneLabel.setText(f"Starting Scene: {scene}")
            self.startingSceneLabel.setAccessibleName(self.startingSceneLabel.text())
            self.startingScene = scene

    def openDirectoryDialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.selectedDirectoryLabel.setText(f"Selected Directory: {directory}")
            self.selectedDirectoryLabel.setAccessibleName(self.selectedDirectoryLabel.text())
            self.selectedDirectory = directory
    
    def getFilePath(self):
        fileName = self.fileNameInput.text()
        if hasattr(self, 'selectedDirectory') and fileName:
            return os.path.join(self.selectedDirectory, f"{fileName}")
        return None
    
    def getStartingScene(self):
        if self.startingScene:
            return self.startingScene
        return None

