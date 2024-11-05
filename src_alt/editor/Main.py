import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QStatusBar, QDialog,
    QMessageBox
)
from PySide6.QtGui import QAction
from projectManager import ProjectManager, ProjectManagerGUI
from HomeMenu import HomeMenu
from SettingsMenu import SettingsMenu
from DirectoryDialogs import OpenFileDialog, PickFilepathDialog
from styles import *
from ProjectMenu import ProjectMenu
from packager import StoryPackager
from variableManagerGUI import VariableManagerDialog
from characterManagerGUI import CharacterManagerDialog
from variableManager import EditorVariableManager
import ui_customize
import keybinds
import speechToText

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600) 
        self.setFixedSize(1280, 720)
        scriptDirectory = os.path.dirname(os.path.abspath(__file__))
        self.projectsDirectory = os.path.join(scriptDirectory, 'projects')  
        if not os.path.exists(self.projectsDirectory):
            os.makedirs(self.projectsDirectory)
        
        # Setup Project Manager
        self.projectManager = ProjectManager(self.projectsDirectory)
        self.projectMenu = ProjectManagerGUI(self.projectManager)
        
        self.projectOpened = False
        
        self.uiSettingsManager = ui_customize.UICustomizeManager(self)
        self.uiSettingsManager.applySettings()
        
        # Main Layout
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.homeMenu = HomeMenu()
        self.settingsMenu = SettingsMenu()
        self.currentFileMenu = None
        self.preferencesMenu = self.uiSettingsManager.menu
        
        self.centralWidget.addWidget(self.homeMenu)
        self.centralWidget.addWidget(self.settingsMenu)
        self.centralWidget.addWidget(self.projectMenu)
        self.centralWidget.addWidget(self.preferencesMenu)
        
        # Menu Bar
        self.initMenuBar()

        self.centralWidget.setCurrentWidget(self.homeMenu)
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)

        self.homeMenu.CreateProject.connect(self.projectMenu.createProject)
        self.homeMenu.OpenExistingProject.connect(self.projectMenu.openExistingProject)
        self.homeMenu.OpenPreferences.connect(self.showPreferencesMenu)
        self.projectMenu.CreateProject.connect(self.onCreateProject)
        self.projectMenu.OpenProject.connect(self.onOpenProject)

        self.updateMenuBar()
        self.initShortcuts()
        
    def initShortcuts(self):
        shortcutsManager = keybinds.ShortcutsManager(self)
        shortcutsManager.addShortcut("Ctrl+Q","Quit",self.close)
        shortcutsManager.addShortcut("Ctrl+/","Replace Shortcuts Menu",lambda: shortcutsManager.openShortcutsMenu())
        shortcutsManager.addShortcut("Ctrl+T","Start Transcription",speechToText.STT.recordCallback)
    
    def initMenuBar(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.openFileAction = QAction("&Open File", self)
        self.startNewProjectAction = QAction("&Start New Project", self)
        self.openExistingProjectAction = QAction("Open Existing &Project", self)
        self.compileProjectAction = QAction("Compile Project", self)
        
        self.fileMenu.addAction(self.openFileAction)
        self.fileMenu.addAction(self.startNewProjectAction)
        self.fileMenu.addAction(self.openExistingProjectAction)
        
        
        self.menusMenu = self.menuBar().addMenu("&Menus")
        self.openHomeAction = QAction("Home", self)
        self.openSettingsAction = QAction("Settings", self)
        self.openPreferencesAction = QAction("Preferences", self)
        self.menusMenu.addAction(self.openHomeAction)
        self.menusMenu.addAction(self.openSettingsAction)
        self.menusMenu.addAction(self.openPreferencesAction)
        
        
        self.optionsMenu = self.menuBar().addMenu("&Options")
        self.openVariableManager = QAction("&Variables", self)
        self.openCharacterManager = QAction("Characters", self)
        self.optionsMenu.addAction(self.openVariableManager)
        self.optionsMenu.addAction(self.openCharacterManager)
        
        # Connect actions to their slots
        self.openFileAction.triggered.connect(self.openFile)
        self.startNewProjectAction.triggered.connect(self.projectMenu.createProject)
        self.openExistingProjectAction.triggered.connect(self.projectMenu.openExistingProject)
        self.openHomeAction.triggered.connect(self.showHomeMenu)
        self.openSettingsAction.triggered.connect(self.showSettingsMenu)
        self.openPreferencesAction.triggered.connect(self.showPreferencesMenu)
        self.compileProjectAction.triggered.connect(self.compileProject)
        self.openVariableManager.triggered.connect(self.showVariableManager)
        self.openCharacterManager.triggered.connect(self.showCharacterManager)

    def updateMenuBar(self):
        self.fileMenu.clear()

        currentWidget = self.centralWidget.currentWidget()

        if isinstance(currentWidget, HomeMenu):
            self.fileMenu.addAction(self.startNewProjectAction)
            self.fileMenu.addAction(self.openExistingProjectAction)
        elif isinstance(currentWidget, ProjectManagerGUI):
            self.fileMenu.addAction(self.openFileAction)
            self.fileMenu.addAction(self.startNewProjectAction)
            self.fileMenu.addAction(self.openExistingProjectAction)
        elif isinstance(currentWidget, ProjectMenu):
            self.fileMenu.addAction(self.compileProjectAction)

    def compileProject(self):
        folderPath = os.path.join(self.projectsDirectory, self.projectManager.currentProject["name"])
        self.dialog = PickFilepathDialog(folderPath)
        if self.dialog.exec() == QDialog.Accepted:
            filePath = self.dialog.getFilePath()
            startingScene = self.dialog.getStartingScene()
            if filePath and startingScene:
                filePath = filePath + ".syoa"
                compiler = StoryPackager()
                compiler.setStartingScene(startingScene)
                compiler.loadStoryFiles(self.projectManager.getCurrentFilePath())
                if compiler.serializeScenes(filePath):
                    QMessageBox.information(self, "Success", f"Compilation complete. Saved to {filePath}")
                else:
                    QMessageBox.warning(self, "Warning", "Compilation failed.")
            else:
                if not startingScene and not filePath:
                    QMessageBox.warning(self, "Please select a starting scene and filepath.")
                if not startingScene:
                    QMessageBox.warning(self, "Please select a starting scene.")
                if not filePath:
                    QMessageBox.warning(self, "Please provide a filepath")

    def updateFileMenu(self, projectName): 
        newFileMenu = ProjectMenu(self.filePathFromName(projectName))
        self.centralWidget.addWidget(newFileMenu)
        self.currentFileMenu = newFileMenu
        self.showFileMenu()

    def openFile(self):
        folderPath = os.path.join(self.projectsDirectory, self.projectManager.currentProject["name"])
        self.fileDialog = OpenFileDialog(folderPath)
        self.fileDialog.show() 
    
    def filePathFromName(self, projectName):
        return os.path.join(self.projectsDirectory, projectName)  
    
    def onCreateProject(self, projectName: str):
        folderPath = os.path.join(self.projectsDirectory, projectName)
        EditorVariableManager(folderPath) # TODO: Make Variable manager clear when opening a different project
        self.projectOpened = True
        self.updateFileMenu(projectName)
    
    def onOpenProject(self, projectName: str):
        folderPath = os.path.join(self.projectsDirectory, projectName)
        EditorVariableManager(folderPath) 
        self.projectOpened = True
        self.updateFileMenu(projectName)
    
    def showVariableManager(self):
        if self.projectOpened:
            self.dialog = VariableManagerDialog(self.projectManager.getCurrentFilePath())
            self.dialog.exec()
        else:
            QMessageBox.warning(self, "Warning", "Open project first.")
    
    def showCharacterManager(self):
        if self.projectOpened:
            self.dialog = CharacterManagerDialog(self.projectManager.getCurrentFilePath())
            self.dialog.exec()
        else:
            QMessageBox.warning(self, "Warning", "Open project first.")
            
    def showFileMenu(self):
        if self.currentFileMenu:
            self.centralWidget.setCurrentWidget(self.currentFileMenu)
            self.updateMenuBar() 
    
    def showHomeMenu(self):
        self.centralWidget.setCurrentWidget(self.homeMenu)
        self.updateMenuBar() 

    def showSettingsMenu(self):
        self.centralWidget.setCurrentWidget(self.settingsMenu)
        self.updateMenuBar()
    
    def showPreferencesMenu(self):
        self.centralWidget.setCurrentWidget(self.preferencesMenu)
        self.updateMenuBar()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
