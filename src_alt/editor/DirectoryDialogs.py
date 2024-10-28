import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QMenuBar, QMessageBox, QListWidget, QPushButton,
    QLineEdit, QLabel, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class ProjectFolderSelectDialog(QDialog):
    def __init__(self, baseDirectory):
        super().__init__()
        self.setWindowTitle("Select a Folder")
        self.setModal(True)

        self.layout = QVBoxLayout(self)

        self.folderList = QListWidget()
        self.layout.addWidget(self.folderList)

        self.selectButton = QPushButton("Select")
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create New File")

        self.layout = QVBoxLayout(self)

        self.fileNameInput = QLineEdit(self)
        self.fileNameInput.setPlaceholderText("Enter filename")
        self.layout.addWidget(QLabel("Filename:"))
        self.layout.addWidget(self.fileNameInput)

        self.directoryButton = QPushButton("Select Directory", self)
        self.layout.addWidget(self.directoryButton)

        self.selectedDirectoryLabel = QLabel("No directory selected", self)
        self.layout.addWidget(self.selectedDirectoryLabel)

        self.okButton = QPushButton("OK", self)
        self.layout.addWidget(self.okButton)

        self.directoryButton.clicked.connect(self.openDirectoryDialog)
        self.okButton.clicked.connect(self.accept)

    def openDirectoryDialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.selectedDirectoryLabel.setText(f"Selected Directory: {directory}")
            self.selectedDirectory = directory

    def getFilePath(self):
        fileName = self.fileNameInput.text()
        if hasattr(self, 'selectedDirectory') and fileName:
            return os.path.join(self.selectedDirectory, f"{fileName}")
        return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(600, 400)
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        openFileAction = QAction("Open File", self)
        openFileAction.triggered.connect(self.openFileMenu)
        fileMenu.addAction(openFileAction)
        
    def openFileMenu(self):
        folder_path = os.path.dirname(os.path.abspath(__file__)) + '//' + "projects" + '//' + "TestProject"
        self.file_dialog = OpenFileDialog(folder_path)
        self.file_dialog.show()

    
if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
