import sys 
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit, QHBoxLayout, QWidget, QLayout
)
from src.editor.parser import *
from pathlib import Path
from src.editor.ProjectMenu import *

class SearchMenuDialog(QDialog):   
    def __init__(self, storyPath=None, currFilePath=None, currProject=None, currProjectMenu=None):
        super().__init__()
        self.setMinimumSize(600, 800)
        #TODO: Error checking on path
        self.changeStoryFolder(storyPath)
        self.changeCurrFile(currFilePath)

        self.currProject = currProject
        self.currTextEdit = currProject.textEditWidget.textEdit
        self.currProjectMenu = currProjectMenu
        

        self.loadSceneLinks()
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("Search Menu")
        self.setAccessibleName("Search Menu")
        self.layout = QVBoxLayout()
        # unsure if outside will be dialog or separate menu, internals should remain same, maybe without QGroupBox wrapper 
        self.mainArea = QGroupBox(self)
        self.mainArea.layout = QVBoxLayout()
        
        self.mainArea.layout.setSpacing(20)

        #insert search text into
        self.searchBox = QGroupBox(self.mainArea)
        self.searchBox.setTitle("Search")
        self.searchBox.layout = QHBoxLayout()
        self.searchBar = QLineEdit(self.searchBox)
        self.searchBar.setAccessibleName("Search field")
        self.searchButton = QPushButton("Search", self.searchBox)
        self.searchButton.setAccessibleName("Search")
        #Connect to function that updates combo boxes based on search



        self.searchBox.layout.addWidget(self.searchBar)
        self.searchBox.layout.addWidget(self.searchButton)
        self.searchBox.setLayout(self.searchBox.layout)

        #results boxes
        #in-file
        self.inFileResultsBox = QGroupBox(self.mainArea)
        self.inFileResultsBox.setTitle("Inside current file")
        self.inFileResultsBox.layout = QHBoxLayout()
        self.inFileResultsDropdown = QComboBox(self.inFileResultsBox)
        self.inFileResultsDropdown.setAccessibleName("In opened files results")        
        self.inFileResultsButton = QPushButton("Go", self.inFileResultsBox)
        self.inFileResultsButton.setAccessibleName("Go to results")
        self.inFileResultsDropdown.setEditable(False)

        self.inFileResultsBox.layout.addWidget(self.inFileResultsDropdown)
        self.inFileResultsBox.layout.addWidget(self.inFileResultsButton)
        self.inFileResultsBox.setLayout(self.inFileResultsBox.layout)

        #link names
        self.linksResultsBox = QGroupBox(self.mainArea)
        self.linksResultsBox.setTitle("Links from current file")
        self.linksResultsBox.layout = QHBoxLayout()
        self.linksResultsDropdown = QComboBox(self.linksResultsBox)
        self.linksResultsDropdown.setAccessibleName("Link names results")
        self.linksResultsButton = QPushButton("Go", self.linksResultsBox)
        self.linksResultsButton.setAccessibleName("Go to results")
        self.linksResultsDropdown.setEditable(False)

        self.linksResultsBox.layout.addWidget(self.linksResultsDropdown)
        self.linksResultsBox.layout.addWidget(self.linksResultsButton)
        self.linksResultsBox.setLayout(self.linksResultsBox.layout)
        
        #in-link results
        self.inLinksResultsBox = QGroupBox(self.mainArea)
        self.inLinksResultsBox.setTitle("Inside linked files")
        self.inLinksResultsBox.layout = QHBoxLayout()
        self.inLinksResultsDropdown = QComboBox(self.inLinksResultsBox)
        self.inLinksResultsDropdown.setAccessibleName("In linked files results")
        self.inLinksResultsButton = QPushButton("Go", self.inLinksResultsBox)
        self.inLinksResultsButton.setAccessibleName("Go to results")
        self.inLinksResultsDropdown.setEditable(False)

        self.inLinksResultsBox.layout.addWidget(self.inLinksResultsDropdown)
        self.inLinksResultsBox.layout.addWidget(self.inLinksResultsButton)
        self.inLinksResultsBox.setLayout(self.inLinksResultsBox.layout)
        

        self.mainArea.layout.addWidget(self.searchBox)
        self.mainArea.layout.addWidget(self.inFileResultsBox)
        self.mainArea.layout.addWidget(self.linksResultsBox)
        self.mainArea.layout.addWidget(self.inLinksResultsBox)
        self.mainArea.setLayout(self.mainArea.layout)
        self.layout.addWidget(self.mainArea)
        self.setLayout(self.layout)

        self.searchBar.textChanged.connect(lambda: self.updateResults(self.searchBar.text()))

        self.searchButton.clicked.connect(lambda: self.updateResults(self.searchBar.text()))

        self.inFileResultsButton.clicked.connect(lambda: self.goToInCurrent(self.inFileResultsDropdown.currentText()))
        self.inLinksResultsButton.clicked.connect(lambda: self.goToInLinked(self.inLinksResultsDropdown.currentText()))
        self.linksResultsButton.clicked.connect(lambda: self.goToLink(self.linksResultsDropdown.currentText()))
        
        self.hide()

    def updateResults(self, query):
        #annotate files with potentially update texts and links
        self.loadSceneLinks()
        self.annotateCurrentFile()
        self.annotateLinkedScenes()

        #Find results from annotated files
        inFileResults = self.findInCurrentFile(query)
        inLinkedResults = self.findInLinkedFiles(query)
        linkedSceneResults = self.findLinkedScenesMatchingName(query)

        #Clear and place results in dropdown menus
        self.inFileResultsDropdown.clear()
        self.inLinksResultsDropdown.clear()
        self.linksResultsDropdown.clear()
        for result in inFileResults:
            self.inFileResultsDropdown.addItem("Line: " + str(result))
        for result in inLinkedResults:
            self.inLinksResultsDropdown.addItem(str(result[0]) + ", Line " + str(result[1]))
        for result in linkedSceneResults:
            self.linksResultsDropdown.addItem(str(result))

    #signals to connect with editor
    def goToInCurrent(self, line):
        if (line != ""):
            lineNum = int(line[5:])
            self.close()
            print([self.currFile, lineNum])
            self.currTextEdit.jumpToLine(lineNum)
            return [self.currFile, lineNum]
    
    def goToInLinked(self, result):
        if (result != ""):
            result = result.split(',')
            sceneName = result[0] + ".txt"
            lineNum = int(result[1][6:])
            self.close()
            print([sceneName, lineNum])
            tab = self.currProjectMenu.tabsWidget.getTabIndex(sceneName)
            if tab is None: #tab is not opened
                targetPath = Path(self.storyDirectory, sceneName)
                self.currProject = self.currProjectMenu.openNewTab(self.storyDirectory)
                self.currProject.openFile(targetPath)

                tab = self.currProjectMenu.tabsWidget.getTabIndex(sceneName)
                self.currProjectMenu.tabsWidget.tabContents.setCurrentIndex(tab)
                self.currProjectMenu.tabsWidget.tabBar.setCurrentIndex(tab)
                self.currTextEdit = self.currProject.textEditWidget.textEdit
            else:
                self.currProjectMenu.tabsWidget.tabContents.setCurrentIndex(tab)
                self.currProjectMenu.tabsWidget.tabBar.setCurrentIndex(tab)
                self.currProject = self.currProjectMenu.tabsWidget.tabContents.currentWidget()
                self.currTextEdit = self.currProject.textEditWidget.textEdit
            self.currTextEdit.jumpToLine(lineNum)
            return [sceneName, lineNum]
    
    def goToLink(self, link):
        if (link != ""):
            self.close()
            print(link + "txt")
            link = link + ".txt"
            tab = self.currProjectMenu.tabsWidget.getTabIndex(link)
            if tab is None: #tab is not opened
                targetPath = Path(self.storyDirectory, link)
                self.currProject = self.currProjectMenu.openNewTab(self.storyDirectory)
                self.currProject.openFile(targetPath)

                tab = self.currProjectMenu.tabsWidget.getTabIndex(link)
                self.currProjectMenu.tabsWidget.tabContents.setCurrentIndex(tab)
                self.currProjectMenu.tabsWidget.tabBar.setCurrentIndex(tab)
                self.currTextEdit = self.currProject.textEditWidget.textEdit
            else:
                self.currProjectMenu.tabsWidget.tabContents.setCurrentIndex(tab)
                self.currProjectMenu.tabsWidget.tabBar.setCurrentIndex(tab)
                self.currProject = self.currProjectMenu.tabsWidget.tabContents.currentWidget()
                self.currTextEdit = self.currProject.textEditWidget.textEdit
            return link 
        

    def changeStoryFolder(self, path):
        self.storyDirectory = Path(path)
    
    def changeCurrFile(self, path):
        self.currFile = Path(self.storyDirectory, path)
        #TODO: ERR checking for nonexistent files
        self.currFilePath = Path(self.storyDirectory, self.currFile)


    #run first
    def loadSceneLinks(self):
        with open(self.currFilePath, 'r') as file:
            self.currFileScript = file.read()
            self.parsedCurr = readScript(self.currFileScript)
            self.sceneLinks = self.parsedCurr.links

    #converts current file into dict of line num/line string pairs
    def annotateCurrentFile(self):
        self.currFileAnnotated = {}
        with open(self.currFilePath, 'r') as file:
            lines = file.read().strip().split("\n")
            index = 1
            for line in lines:
                self.currFileAnnotated[index] = line
                index += 1

    #converts all linked files into dict of dicts of line num/line string pairs
    def annotateLinkedScenes(self):
        self.linkedScenesAnnotated = {}
        for scene in self.sceneLinks:
            with open(Path(self.storyDirectory, scene + ".txt")) as file:
                annotations = {}
                lines = file.read().strip().split("\n")
                index = 1
                for line in lines:
                    annotations[index] = line
                    index += 1
                self.linkedScenesAnnotated[scene] = annotations


    #takes query for current file, returns line(s) it occurs
    def findInCurrentFile(self, query):
        results = []
        if (query == ""):
            return results
        query = query.lower()
        for number, line in self.currFileAnnotated.items():
            searched_line = line.lower()
            if query in searched_line:
                results.append(number)
        return results
    
    #returns list of lists where first element is scene name, second is line number with match
    def findInLinkedFiles(self, query):
        results = []
        if (query == ""):
            return results
        query = query.lower()
        for scene, lines in self.linkedScenesAnnotated.items():
            for number, line in lines.items():
                searched_line = line.lower()
                if query in searched_line:
                    results.append([scene, number])
        return results
    
    #finds name of linked scene matching query
    def findLinkedScenesMatchingName(self, query):
        results = []
        if (query == ""):
            return results
        query = query.lower()
        for link in self.sceneLinks:
            searched_link = link.lower()
            if query in searched_link:
                results.append(link)
        return results

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exit(app.exec())