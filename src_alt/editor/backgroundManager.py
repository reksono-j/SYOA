import os, shutil, re
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton, QInputDialog, QMessageBox, QFileDialog, QListWidgetItem
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from singleton import Singleton
from projectManager import ProjectManager

class BackgroundManager(metaclass=Singleton):
    def __init__(self):
        self.projectManager = ProjectManager()
        self.path = None
        self.projectManager.changedProject.connect(self.updatePath)
        self.updatePath()

    def updatePath(self):
        projectPath = self.projectManager.getCurrentFilePath()
        self.path = os.path.join(projectPath, "backgrounds")
        os.makedirs(self.path, exist_ok=True)

    def addBackground(self, filePath):
        if not filePath.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValueError("Only .png, .jpg, or .jpeg files are allowed.")

        baseName = os.path.splitext(os.path.basename(filePath))[0]
        if self.backgroundExists(baseName):
            raise FileExistsError(f"A background with the name '{baseName}' already exists (ignoring file extension).")

        destPath = os.path.join(self.path, os.path.basename(filePath))
        shutil.copy(filePath, destPath)
        return destPath

    def renameBackground(self, originalFileName, newName):
        if not re.match(r'^[a-zA-Z0-9_-]+$', newName):
            raise ValueError("Name must contain only alphanumeric characters, dashes, or underscores.")

        baseName, ext = os.path.splitext(originalFileName)
        if self.backgroundExists(newName):
            raise FileExistsError(f"A background with the name '{newName}' already exists (ignoring file extension).")

        originalPath = os.path.join(self.path, originalFileName)
        newPath = os.path.join(self.path, f"{newName}{ext}")

        os.rename(originalPath, newPath)
        return newPath

    def backgroundExists(self, baseName):
        for fileName in os.listdir(self.path):
            fileBaseName, _ = os.path.splitext(fileName)
            if fileBaseName.lower() == baseName.lower():
                return True
        return False
    
    def getBackgroundFilePathByBaseName(self, baseName):
        for fileName in os.listdir(self.path):
            fileBaseName, ext = os.path.splitext(fileName)
            if fileBaseName.lower() == baseName.lower() and ext.lower() in ['.png', '.jpg', '.jpeg']:
                return os.path.join(self.path, fileName)
        raise FileNotFoundError(f"Background with the basename '{baseName}' not found.")

class BackgroundManagerDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.backgroundManager = BackgroundManager()

        self.setWindowTitle("Background Manager")
        self.resize(400, 300)

        self.listWidget = QListWidget()
        self.addButton = QPushButton("Add Background")
        self.renameButton = QPushButton("Rename Selected")

        self.addButton.clicked.connect(self.addBackground)
        self.renameButton.clicked.connect(self.renameSelectedBackground)

        layout = QVBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.renameButton)
        self.setLayout(layout)

        self.populateList()

    def populateList(self):
        self.listWidget.clear()
        if os.path.isdir(self.backgroundManager.path):
            for fileName in os.listdir(self.backgroundManager.path):
                if fileName.lower().endswith(('.png', '.jpg', '.jpeg')):
                    listItem = QListWidgetItem(fileName)
                    pixmap = QPixmap(os.path.join(self.backgroundManager.path, fileName))
                    listItem.setIcon(pixmap.scaled(50, 50, Qt.KeepAspectRatio))
                    self.listWidget.addItem(listItem)

    def addBackground(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Add Background", "", "Image Files (*.png *.jpg *.jpeg)")
        if filePath:
            try:
                self.backgroundManager.addBackground(filePath)
                self.populateList()
            except ValueError as e:
                QMessageBox.warning(self, "Invalid File", str(e))

    def renameSelectedBackground(self):
        selectedItems = self.listWidget.selectedItems()
        if not selectedItems:
            QMessageBox.warning(self, "No Selection", "Please select a background to rename.")
            return

        originalFileName = selectedItems[0].text()
        newName, ok = QInputDialog.getText(self, "Rename Background", "Enter a new name (alphanumeric, no spaces):")
        if ok and newName:
            try:
                self.backgroundManager.renameBackground(originalFileName, newName)
                self.populateList()
            except (ValueError, FileExistsError) as e:
                QMessageBox.warning(self, "Invalid Name", str(e))