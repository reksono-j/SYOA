import os
import re
import json
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QInputDialog, QDialog
)
from PySide6.QtCore import Signal, QObject
from src_alt.editor.DirectoryDialogs import ProjectFolderSelectDialog

class ProjectManager(QObject):
    changedProject = Signal()
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProjectManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, baseDirectory=None):
        if hasattr(self, 'initialized') and self.initialized:
            return
        super().__init__()
        
        if baseDirectory is not None:
            self.baseDirectory = baseDirectory
            if not os.path.exists(self.baseDirectory):
                os.makedirs(self.baseDirectory)
        
        self.projects = []
        self.currentProject = {}
        self.initialized = True

        
    def createProject(self, projectName):
        if not self.isValidProjectName(projectName):
            raise ValueError("Invalid project name. Must be alphanumeric with underscores.")
        
        projectPath = os.path.join(self.baseDirectory, projectName)
        if os.path.exists(projectPath):
            raise FileExistsError("Project already exists.")
        os.makedirs(projectPath)

        # TODO : Add other useful info
        metadata = {
            "name": projectName,
            "createdAt": str(datetime.now())
        }
        
        with open(os.path.join(projectPath, "project.json"), 'w') as f:
            json.dump(metadata, f)
        self.currentProject = metadata 
        self.changedProject.emit()
        return metadata

    def getCurrentFilePath(self):
        return os.path.join(self.baseDirectory, self.currentProject['name'])
    
    # TODO: Figure out a good place to use this
    def setStartScene(self, sceneName):
        self.currentProject['startScene'] = sceneName
        projectPath = os.path.join(self.baseDirectory, self.currentProject['name'])
        with open(os.path.join(projectPath, "project.json"), 'w') as f:
            json.dump(self.currentProject, f)

    @staticmethod
    def isValidProjectName(projectName):
        return bool(re.match("^[A-Za-z0-9_]+$", projectName))

    def loadProject(self, projectName):
        projectPath = os.path.join(self.baseDirectory, projectName)
        with open(os.path.join(projectPath, "project.json"), 'r') as f:
            metadata = json.load(f)
        self.currentProject = metadata  
        self.changedProject.emit()
        return metadata
    
    def listProjects(self):
        self.projects = [d for d in os.listdir(self.baseDirectory) if os.path.isdir(os.path.join(self.baseDirectory, d))]
        return self.projects

class ProjectManagerGUI(QWidget):
    CreateProject = Signal(str)
    OpenProject = Signal(str)
    
    def __init__(self, projectManager):
        super().__init__()
        self.projectManager = projectManager
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Project Manager')
        layout = QVBoxLayout()

        self.projectList = QListWidget()
        layout.addWidget(self.projectList)

        self.createButton = QPushButton('Create Project')
        self.createButton.clicked.connect(self.createProject)
        layout.addWidget(self.createButton)

        self.loadButton = QPushButton('Load Project')
        self.loadButton.clicked.connect(self.loadProject)
        layout.addWidget(self.loadButton)

        self.setLayout(layout)
        self.refreshProjectList()

    def refreshProjectList(self):
        self.projectList.clear()
        projects = self.projectManager.listProjects()
        self.projectList.addItems(projects)

    def createProject(self):
        projectName, ok = QInputDialog.getText(self, 'Create Project', 'Enter project name:')
        if ok and projectName:
            try:
                self.projectManager.createProject(projectName)
                self.refreshProjectList()
                self.CreateProject.emit(projectName)
                QMessageBox.information(self, "Success", f"Project '{projectName}' created successfully.")
            except FileExistsError as e:
                QMessageBox.critical(self, "Error", str(e))

    def loadProject(self):
        currentItem = self.projectList.currentItem()
        if currentItem:
            projectName = currentItem.text()
            metadata = self.projectManager.loadProject(projectName)
            QMessageBox.information(self, "Project Loaded", f"Loaded project: {metadata['name']}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a project to load.")
    
    def openExistingProject(self):
        dialog = ProjectFolderSelectDialog(self.projectManager.baseDirectory)
        if dialog.exec() == QDialog.Accepted:
            metadata = self.projectManager.loadProject(dialog.getSelectedFolder())
            self.OpenProject.emit(os.path.join(self.projectManager.baseDirectory,metadata["name"]))
            QMessageBox.information(self, "Project Loaded", f"Loaded project: {metadata['name']}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a project to load.")
    

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    baseDirectory = scriptDirectory + '\\' +'projects'  
    if not os.path.exists(baseDirectory):
        os.makedirs(baseDirectory)

    window = ProjectManagerGUI(baseDirectory)
    window.show()
    sys.exit(app.exec())
