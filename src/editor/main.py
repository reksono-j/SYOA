import sys
import os
from PySide6.QtCore import (
    Qt, QThread, Signal
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QStatusBar, 
    QDialog, QMessageBox, QProgressDialog
)
from PySide6.QtGui import QAccessibleValueChangeEvent, QAction, QAccessible, QKeySequence, QAccessibleEvent

script_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.editor.projectManager import ProjectManager, ProjectManagerGUI
from src.editor.HomeMenu import HomeMenu
from src.editor.SettingsMenu import SettingsMenu
from src.editor.DirectoryDialogs import OpenFileDialog, PickFilepathDialog
from src.editor.styles import *
from src.editor.ProjectMenu import ProjectMenu, ProjectFileMenu
from src.editor.packager import StoryPackager
from src.editor.customAudio import AudioManagerDialog
from src.editor.characterManager import CharacterManagerDialog
from src.editor.variableManagerGUI import VariableManagerDialog
from src.editor.backgroundManager import BackgroundManagerDialog
from src.editor.handhold import HandHoldManager
from src.editor.search import SearchMenuDialog
from src.editor.customAudio import CustomAudio
from src.editor.numberedTextEdit import NumberedTextEdit
from src.editor.ui_customize import *
from src.editor.keybinds import *
from src.editor.speechToText import *
from src.editor.tutorial import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600) 
        self.setFixedSize(1280, 720)
        self.setWindowTitle("Speak Your Own Adventure")
        scriptDirectory = os.path.dirname(os.path.abspath(__file__))
        self.projectsDirectory = os.path.join(scriptDirectory, 'projects')  
        if not os.path.exists(self.projectsDirectory):
            os.makedirs(self.projectsDirectory)
        
        # Setup Project Manager
        self.projectManager = ProjectManager(self.projectsDirectory)
        self.projectMenu = ProjectManagerGUI(self.projectManager)
        
        self.projectOpened = False
        
        self.uiSettingsManager = UICustomizeManager(self)
        self.uiSettingsManager.applySettings()
        
        self.handholdManager = HandHoldManager()
        
        # Main Layout
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.homeMenu = HomeMenu()
        #self.settingsMenu = SettingsMenu()
        self.currentFileMenu = None
        self.preferencesMenu = self.uiSettingsManager.menu
        
        self.centralWidget.addWidget(self.homeMenu)
        #self.centralWidget.addWidget(self.settingsMenu)
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
        self.homeMenu.ShowTutorial.connect(self.showTutorial)
        self.projectMenu.CreateProject.connect(self.onCreateProject)
        self.projectMenu.OpenProject.connect(self.onOpenProject)

        self.updateMenuBar()
        self.initShortcuts()
        
    def initShortcuts(self):
        shortcutsManager = ShortcutsManager(self)
        shortcutsManager.addShortcut("Ctrl+Q","Quit",self.close)
        shortcutsManager.addShortcut("Ctrl+/","Replace Shortcuts Menu",lambda: shortcutsManager.openShortcutsMenu())
        shortcutsManager.addShortcut("Ctrl+T","Start Transcription", STT.recordCallback)
        shortcutsManager.addShortcut("Ctrl+F","Open Search Menu",self.showSearchMenu)
        shortcutsManager.addShortcut("Alt+C", "Type CHOICE", lambda: self.insertTextIntoIDE("CHOICE "))
        shortcutsManager.addShortcut("Alt+B", "Type BRANCH", lambda: self.insertTextIntoIDE("BRANCH "))
        shortcutsManager.addShortcut("Alt+E", "Type END", lambda: self.insertTextIntoIDE("END "))
        shortcutsManager.addShortcut("Alt+M", "Type MODIFY", lambda: self.insertTextIntoIDE("MODIFY "))
        shortcutsManager.addShortcut("Alt+S", "Type SFX", lambda: self.insertTextIntoIDE("SFX "))
        shortcutsManager.addShortcut("Alt+V", "Type BGM", lambda: self.insertTextIntoIDE("BGM "))
        
        
        shortcutsManager.addShortcut("Ctrl+Y","Open Tutorial",self.showTutorial)
    
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
        #self.openSettingsAction = QAction("Settings", self)
        self.openPreferencesAction = QAction("Preferences", self)
        self.menusMenu.addAction(self.openHomeAction)
        #self.menusMenu.addAction(self.openSettingsAction)
        self.menusMenu.addAction(self.openPreferencesAction)
        
        
        self.optionsMenu = self.menuBar().addMenu("&Options")
        self.openAudioManager = QAction("Audio", self)
        self.openCharacterManager = QAction("Characters", self)
        self.openVariableManager = QAction("Variables", self)
        self.openBackgroundManager = QAction("Background", self)
        self.openHandholdManager = QAction("Handhold Assistant", self)
        self.openAudioManager.setShortcut(QKeySequence("alt+j"))       # Shortcut: Audio Manager
        self.openCharacterManager.setShortcut(QKeySequence("alt+l")  ) # Shortcut: Character Manager
        self.openVariableManager.setShortcut(QKeySequence("alt+k"))    # Shortcut: Variable Manager
        self.openBackgroundManager.setShortcut(QKeySequence("alt+;"))  # Shortcut: Background Manager
        self.openHandholdManager.setShortcut(QKeySequence("alt+h"))    # Shortcut: Handhold Manager
        self.optionsMenu.addAction(self.openAudioManager)
        self.optionsMenu.addAction(self.openCharacterManager)
        self.optionsMenu.addAction(self.openVariableManager)
        self.optionsMenu.addAction(self.openBackgroundManager)
        self.optionsMenu.addAction(self.openHandholdManager)
        
        # Connect actions to their slots
        self.openFileAction.triggered.connect(self.openFile)
        self.startNewProjectAction.triggered.connect(self.projectMenu.createProject)
        self.openExistingProjectAction.triggered.connect(self.projectMenu.openExistingProject)
        self.openHomeAction.triggered.connect(self.showHomeMenu)
        #self.openSettingsAction.triggered.connect(self.showSettingsMenu)
        self.openPreferencesAction.triggered.connect(self.showPreferencesMenu)
        self.compileProjectAction.triggered.connect(self.compileProject)
        self.openAudioManager.triggered.connect(self.showAudioManager)
        self.openCharacterManager.triggered.connect(self.showCharacterManager)
        self.openVariableManager.triggered.connect(self.showVariableManager)
        self.openBackgroundManager.triggered.connect(self.showBackgroundManager)
        self.openHandholdManager.triggered.connect(self.showHandholdManager)
        
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
        if not self.projectOpened:
            QMessageBox.warning(self, "Error", "No project is currently opened.")
            return
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

                # Progress dialog kept disappearing and reappearing. This stops that from happening
                if not hasattr(self, 'progressDialog') or self.progressDialog is None:
                    self.progressDialog = QProgressDialog("Compiling project...", "Cancel", 0, 100, self)
                self.progressDialog.setWindowModality(Qt.WindowModal)
                self.progressDialog.setAutoClose(False)
                self.progressDialog.setAutoReset(False)
                
                def announceProgress(value):
                    self.progressDialog.setValue(value)
                    event = QAccessibleValueChangeEvent(self.progressDialog, value)
                    QAccessible.updateAccessibility(event)
                
                def handleCompilation(success):
                    self.progressDialog.close() 
                    self.progressDialog.deleteLater()
                    self.progressDialog = None
                    if success:
                        QMessageBox.information(self, "Success", f"Compilation complete. Saved to {filePath}")
                    else:
                        QMessageBox.warning(self, "Warning", "Compilation failed.")
                        

                
                self.thread = CompileThread(compiler, filePath)

                self.thread.progressUpdated.connect(announceProgress)
                self.thread.serializationComplete.connect(lambda success: handleCompilation(success))
                self.thread.start()

                self.progressDialog.canceled.connect(self.thread.terminate)
                self.progressDialog.exec()
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
        self.projectOpened = True
        self.updateFileMenu(projectName)
    
    def onOpenProject(self, projectName: str):
        self.projectOpened = True
        self.updateFileMenu(projectName)
    
    def showVariableManager(self):
        self.showManagerDialog(VariableManagerDialog)
    
    def showCharacterManager(self):
        self.showManagerDialog(CharacterManagerDialog)
            
    def showAudioManager(self):
        self.showManagerDialog(AudioManagerDialog)
    
    def showBackgroundManager(self):
        self.showManagerDialog(BackgroundManagerDialog)
    
    def showManagerDialog(self, _dialog):
        if self.projectOpened:
            dialog = _dialog()
            dialog.setStyleSheet(self.uiSettingsManager.getTheme())
            dialog.exec()
        else:
            QMessageBox.warning(self, "Warning", "Open project first.")
    
    def showHandholdManager(self):
        self.handholdManager.menuToggle()
        
    def showFileMenu(self):
        if self.currentFileMenu:
            self.centralWidget.setCurrentWidget(self.currentFileMenu)
            self.updateMenuBar() 
    
    def showHomeMenu(self):
        self.projectOpen = False
        self.centralWidget.setCurrentWidget(self.homeMenu)
        self.updateMenuBar() 

    # def showSettingsMenu(self):
    #     self.centralWidget.setCurrentWidget(self.settingsMenu)
    #     self.updateMenuBar()
    
    def showPreferencesMenu(self):
        self.centralWidget.setCurrentWidget(self.preferencesMenu)
        self.updateMenuBar()

    def showSearchMenu(self):
        #Move logic into search.py
        currentWidget = self.centralWidget.currentWidget()

        if isinstance(currentWidget, ProjectMenu):
            projectFileMenu = currentWidget.tabsWidget.getTabWidget(currentWidget.tabsWidget.tabBar.currentIndex())

            if isinstance(projectFileMenu, ProjectFileMenu):
                openProject = projectFileMenu
                openScene = projectFileMenu.textEditWidget
                openScenePath = openScene.currentFile
                openScene.saveFile()
                if openScene and openScenePath:
                    self.dialog = SearchMenuDialog(self.projectManager.getCurrentFilePath(), openScenePath, openProject, currentWidget)
                    self.dialog.exec()
                else:
                    QMessageBox.warning(self, "Warning", "Open scene first.")

    def showTutorial(self):
        self.dialog = TutorialDialog()
        self.dialog.exec()
    
    def insertTextIntoIDE(self, text):
        currentWidget = QApplication.focusWidget()
        
        if isinstance(currentWidget, NumberedTextEdit):
            cursor = currentWidget.textCursor()
            cursor.insertText(text)
            
            accessible_event = QAccessibleEvent(currentWidget, QAccessible.Event.TextInserted)
            QAccessible.updateAccessibility(accessible_event)
                
class CompileThread(QThread):
    progressUpdated = Signal(int)  
    errorOccurred = Signal(str)   
    serializationComplete = Signal(bool)  

    def __init__(self, packager: StoryPackager, filepath: str, parent=None):
        super().__init__(parent)
        self.packager = packager
        self.filepath = filepath

    def run(self):
        try:
            success = self.packager.serializeScenes(self.filepath, progressCallback=self.progressUpdated.emit)  
            self.serializationComplete.emit(success)
        except Exception as e:
            if e:
                self.errorOccurred.emit(str(e))
            print(e)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
