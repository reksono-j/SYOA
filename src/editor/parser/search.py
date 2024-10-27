import sys 
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import fuzzyfinder
from packager import storyPackager
from pathlib import Path
import io
import os

class SearchMenu(QWidget):
    def __init__(self, SearchMenu, parent):
        super(SearchMenu, self).__init__(parent)
        self.parent = parent
        self.SearchManager = SearchManager
        self.initParameters()
        self.initUI()

    def initParameters(self):
        #parameters something
        return 1

    def initUI(self):
        self.setTitle("Search Menu")

        # unsure if outside will be dialog or separate menu, internals should remain same, maybe without QGroupBox wrapper 
        self.mainArea = QGroupBox(self)
        self.mainArea.layout = QVBoxLayout()
        self.mainArea.layout.setSpacing(20)

        #insert search text into
        self.searchBox = QGroupBox(self.mainArea)
        self.searchBar = QLineEdit(self.searchBox)
        self.searchButton = QPushButton("Search", self.searchBox)
        #Connect to function that updates combo boxes based on search
        self.searchButton.clicked.connect(lambda: self.updateResults(self.searchBar.text()))

        #results boxes
        self.inFileResultsBox = QGroupBox(self.mainArea)
        self.inFileResultsDropdown = QComboBox(self.inFileResultsBox)
        self.inFileResultsButton = QPushButton("Go", self.inFileResultsBox)
        self.inFileResults.setEditable(False)

        self.linksResultsBox = QComboBox(self.mainArea)
        self.linksResultsDropdown = QComboBox(self.linksResultsBox)
        self.linksResultsButton = QPushButton("Go", self.linksResultsBox)
        self.linksResults.setEditable(False)
        
        self.inLinksResultsBox = QComboBox(self.mainArea)
        self.inLinksResultsDropdown = QComboBox(self.inLinksResultsBox)
        self.inLinksResultsButton = QPushButton("Go", self.inLinksResultsBox)
        self.inLinksResults.setEditable(False)

        # set up accessibility

        # typing box

        # group box with vertical alignment of three search types - 1. In file 2.Links (compile first?) 3. In other files that are linked

        # Pop up that is an overlay that takes focus and has a text box in middle

        # Removes pop up on focus lost?

        # Maybe as a QDialog?

    def onOpen(self):
        self.open()
        self.loadSceneLinks()

    def updateResults(self, query):
        self.searchManager.annotateCurrentFile()
        self.searchManager.annotateLinkedScenes()
        inFileResults = self.searchManager.findInCurrentFile(query)
        inLinkedResults = self.searchManager.findInLinkedFiles(query)
        linkedSceneResults = self.searchManager.findLinkedScenesMatchingName(query)
        for result in inFileResults:
            self.inFileResultsDropdown.addItem("Line: " + str(result))
        for result in inLinkedResults:
            self.inLinksResultsDropdown.addItem("Scene: " + str(result[0]) + ", Line: " + str(result[1]))
        for result in linkedSceneResults:
            self.linksResultsDropdown.addItem(str(result))





class SearchManager:
    def __init__(self, window) -> None:
        self.window = window
        self.menu = SearchManager(self, window)
        self.storyDirectory = Path(Path.cwd(), Path("Story_EX_DeleteLater")) #TODO:Change this default
        self.currFile = "Scene1.txt"
        self.currFilePath = Path(self.storyDirectory, self.currFile)
        self.packager = storyPackager

    def changeStoryFolder(self, path):
        self.storyDirectory = Path(path)
    
    def changeCurrFile(self, path):
        self.currFile = Path(self.storyDirectory, path)
        #TODO: err checking for nonexistent files
        self.currFilePath = Path(self.storyDirectory, self.currFile)


    #run first
    def loadSceneLinks(self):
        storyDirectory = self.storyDirectory
        self.packager.loadStoryFilesFromDirectory()
        self.sceneLinks = []
        for scene in self.packager.rawScenes:
            if ((scene.name + ".txt") == self.currFile): 
                self.sceneLinks = self.packager._serializeScene['links']

    #converts current file into dict of line num/line string pairs
    def annotateCurrentFile(self):
        self.currFileAnnotated = {}
        with open(self.currFilePath) as file:
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
                    self.annotations[index] = line
                    index += 1
                self.linkedScenesAnnotated[scene] = annotations


    #takes query for current file, returns line(s) it occurs
    def findInCurrentFile(self, query):
        results = []
        for line in self.currFileAnnotated.items():
            matches = fuzzyfinder(query, line[1])
            if (len(matches) != 0):
                results.append(line[0])
        return results
    
    #returns list of lists where first element is scene name, second is line number with match
    def findInLinkedFiles(self, query):
        results = []
        for scene in self.linkedScenesAnnotated.items():
            for line in scene[1]:
                matches = fuzzyfinder(query, line[1])
                if (len(matches) != 0):
                    results.append([scene[0], line[0]])
        return results
    
    #finds name of linked scene matching query
    def findLinkedScenesMatchingName(self, query):
        results = []
        for link in self.sceneLinks:
            matches = fuzzyfinder(query, link)
            if (len(matches) != 0):
                results.append(link)
        return results
