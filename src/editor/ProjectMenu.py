import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget,
    QListWidgetItem, QPushButton, QInputDialog, QMessageBox, QStackedWidget,
)
from PySide6.QtCore import Signal, Qt
from src.editor.numberedTextEdit import NumberedTextEdit
from src.editor.Tabs import TabsWidget

class ProjectMenu(QWidget):
    def __init__(self, folderPath):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.tabsWidget = TabsWidget()
        self.layout.addWidget(self.tabsWidget)

        self.addTabButton = QPushButton("Open Another File Tab")
        self.addTabButton.clicked.connect(lambda: self.openNewTab(folderPath))
        self.layout.addWidget(self.addTabButton)

        self.openNewTab(folderPath)
        self.setupFocusOrder()
        
    def setupFocusOrder(self):
        for index in range(self.tabsWidget.tabBar.count()):
            projectFileMenu = self.tabsWidget.getTabWidget(index)

            if isinstance(projectFileMenu, ProjectFileMenu):
                fileListWidget = projectFileMenu.fileListWidget.fileListWidget
                textEdit = projectFileMenu.textEditWidget.textEdit
                saveButton = projectFileMenu.textEditWidget.saveButton
                closeButton = projectFileMenu.textEditWidget.closeButton
                
                self.setTabOrder(self.tabsWidget.tabBar, fileListWidget)
                self.setTabOrder(fileListWidget, textEdit)
                self.setTabOrder(textEdit, saveButton)
                self.setTabOrder(saveButton, closeButton)
                self.setTabOrder(closeButton, self.tabsWidget.tabBar)
                self.setTabOrder(self.addTabButton, self.tabsWidget.tabBar)
                
    def openNewTab(self, folderPath):
        projectFileMenu = ProjectFileMenu(folderPath)

        projectFileMenu.textEditWidget.fileLoaded.connect(lambda filename: self.updateTabTitle(projectFileMenu, filename))
        projectFileMenu.textEditWidget.fileClosed.connect(lambda: self.resetTabTitle(projectFileMenu))
        projectFileMenu.fileListWidget.newFileCreated.connect(self.updateFileLists)
        projectFileMenu.textEditWidget.installEventFilter(self)
        
        tabIndex = self.tabsWidget.tabBar.count() 
        tabTitle = f"File {tabIndex + 1}"
        self.tabsWidget.addTab(tabTitle, projectFileMenu)
        
        self.setupFocusOrder()
        return projectFileMenu


    def updateFileLists(self):
        for tab in self.tabsWidget.getAllTabs():
            tab[1].fileListWidget.populateFileList()
    
    def updateTabTitle(self, projectFileMenu, filename):
        tabIndex = self.tabsWidget.tabContents.indexOf(projectFileMenu)
        if tabIndex != -1:
            self.tabsWidget.tabBar.setTabText(tabIndex, filename)

    def resetTabTitle(self, projectFileMenu):
        tabIndex = self.tabsWidget.tabContents.indexOf(projectFileMenu)
        if tabIndex != -1:
            originalTitle = f"File {tabIndex + 1}" 
            self.tabsWidget.tabBar.setTabText(tabIndex, originalTitle)


class ProjectFileMenu(QMainWindow):
    def __init__(self, folderPath):
        super().__init__()
        self.setWindowTitle("Project File Menu")
        self.setAccessibleName("Project File Menu")

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # File List Layer
        self.fileListWidget = FileListWidget(folderPath, self.openFile)
        self.stackedWidget.addWidget(self.fileListWidget)

        # Text Edit Layer
        self.textEditWidget = TextEditWidget(self.closeFile)
        self.stackedWidget.addWidget(self.textEditWidget)

        self.stackedWidget.setCurrentWidget(self.fileListWidget) 

        # track currently opened files
        self.openedFiles = set()


    def openFile(self, fullPath):
        if fullPath in self.openedFiles:
            QMessageBox.warning(self, "File Already Open", f"The file '{os.path.basename(fullPath)}' is already open.")
            return

        self.openedFiles.add(fullPath)  # Mark file as open
        self.textEditWidget.loadFile(fullPath)
        self.stackedWidget.setCurrentWidget(self.textEditWidget)  # Switch to the text editor

    def closeFile(self):
        self.openedFiles.discard(self.textEditWidget.currentFile)  # Remove file from set
        self.stackedWidget.setCurrentWidget(self.fileListWidget)  # Switch back to the file list

class FileListWidget(QWidget):
    newFileCreated = Signal()
    
    def __init__(self, folderPath, openFileCallback):
        super().__init__()
        self.folderPath = folderPath
        self.setContentsMargins(0,0,0,0)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.fileListWidget = QListWidget()
        self.fileListWidget.setAccessibleName("File List")

        self.populateFileList()

        self.createFileButton = QPushButton("Create New Scene")
        self.createFileButton.setAccessibleName("Create New Scene")
        self.createFileButton.clicked.connect(self.createNewFile)

        self.layout.addWidget(self.fileListWidget)
        self.layout.addWidget(self.createFileButton)
        self.setLayout(self.layout)

        self.fileListWidget.itemActivated.connect(self.handleFileInteraction)

        self.openFileCallback = openFileCallback

    def populateFileList(self):
        self.fileListWidget.clear()
        if os.path.exists(self.folderPath) and os.path.isdir(self.folderPath):
            for fileName in os.listdir(self.folderPath):
                if fileName.endswith('.txt'):
                    listItem = QListWidgetItem(os.path.splitext(fileName)[0])
                    self.fileListWidget.addItem(listItem)

    def createNewFile(self):
        fileName, ok = QInputDialog.getText(self, "Create New File", "Enter file name:")
        if ok and fileName:
            fullPath = os.path.join(self.folderPath, f"{fileName}.txt")
            if not os.path.exists(fullPath):
                with open(fullPath, 'w') as file:
                    file.write("")
                QMessageBox.information(self, "File Created", f"File '{fileName}.txt' has been created.")
                # self.populateFileList()
                self.newFileCreated.emit()
            else:
                QMessageBox.warning(self, "File Exists", f"File '{fileName}.txt' already exists.")

    def handleFileInteraction(self, item):
        fileName = item.text()
        fullPath = os.path.join(self.folderPath, f"{fileName}.txt")
        self.openFileCallback(fullPath)  # Use callback to open the file


class TextEditWidget(QWidget):
    fileLoaded = Signal(str)
    fileClosed = Signal()   

    def __init__(self, fileClosedCallback):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.textEdit = NumberedTextEdit()
        self.layout.addWidget(self.textEdit)

        self.saveButton = QPushButton("Save Scene")
        self.saveButton.setAccessibleName("Save Scene")
        self.saveButton.clicked.connect(self.saveFile)
        self.closeButton = QPushButton("Close File")
        self.closeButton.setAccessibleName("Close File")
        self.closeButton.clicked.connect(self.closeFile)

        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.closeButton)

        self.currentFile = None
        self.isModified = False
        self.fileClosedCallback = fileClosedCallback

        self.textEdit.textChanged.connect(self.onTextChanged)

    def loadFile(self, fullPath):
        self.currentFile = fullPath
        try:
            with open(fullPath, 'r') as file:
                self.textEdit.setPlainText(file.read())
                self.isModified = False  # Reset modified status on load
                self.fileLoaded.emit(os.path.basename(fullPath))  # Emit the file name when loaded
        except Exception as e:
            QMessageBox.critical(self, "Error Opening File", f"An error occurred: {str(e)}")

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Tab and event.modifiers() == Qt.ControlModifier:
            event.accept()
            self.focusNextChild()
        else:
            super().keyPressEvent(event)
    
    def saveFile(self):
      if self.currentFile:
        try:
            with open(self.currentFile, 'w') as file:
                file.write(self.textEdit.toPlainText())
                self.isModified = False  # Reset modified status on save
                QMessageBox.information(self, "File Saved", f"File '{os.path.basename(self.currentFile)}' has been saved.")
        except Exception as e:
            QMessageBox.critical(self, "Error Saving File", f"An error occurred: {str(e)}")

    def closeFile(self):
        if self.isModified:
            reply = QMessageBox.question(self, "Unsaved Changes", "You have unsaved changes. Are you sure you want to close?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        self.fileClosed.emit()
        self.fileClosedCallback()  
        self.textEdit.clear()
        self.currentFile = None 

    def onTextChanged(self):
        self.isModified = True
        
    def getCurrentFile(self):
        return self.currentFile

