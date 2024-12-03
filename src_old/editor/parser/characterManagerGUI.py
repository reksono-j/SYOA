import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QScrollArea, QDialog, QLineEdit
)
from speakerForm import *
import json
import os

class CharacterManagerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # List Title
        self.label = QLabel("Character List")
        self.label.setAccessibleName("Character List")
        self.layout.addWidget(self.label)

        # Area where characters are
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)  
        self.scrollArea.setAccessibleName("Character list")

        # Widget that holds a name
        self.nameContainer = QWidget()  
        self.nameLayout = QVBoxLayout(self.nameContainer)  
        self.scrollArea.setWidget(self.nameContainer)  
        self.layout.addWidget(self.scrollArea)

        # Add button
        self.addButton = QPushButton("Add Name")
        self.addButton.setAccessibleName("Add Name Button")
        self.addButton.clicked.connect(self.addCharacter)
        self.layout.addWidget(self.addButton)

        # Close button
        self.closeButton = QPushButton("Close")
        self.closeButton.setAccessibleName("Close Button")
        self.closeButton.clicked.connect(self.onClose)
        self.layout.addWidget(self.closeButton)

        self.setLayout(self.layout)
        self.setWindowTitle("Character Manager")

        self.characters = []
    
    def addCharacter(self):
        name = self.openNameDialog()
        if not name:
            return
        self.characters.append([name, []])
        self.addAliasRow(name)
    
    def isPresent(self, name) -> bool:
        if self.characters:
            i = next((i for i, character in enumerate(self.characters) if character[0] == name), -1)
            return i != -1
        else:
            return False
    
    def addAliasRow(self, name):
        nameLayout = QHBoxLayout()
        nameLabel = QLabel(name)
        nameLabel.setAccessibleName(f"Name: {name}")  
        editButton = QPushButton("Edit")
        editButton.setAccessibleName(f"Edit {name} Button")  
        editButton.clicked.connect(lambda: self.editName(name))
        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(lambda: self.deleteCharacter(name, nameLayout))
        deleteButton.setAccessibleName(f"Delete {name} Button")
        
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(editButton)
        nameLayout.addWidget(deleteButton)
        self.nameLayout.addLayout(nameLayout)  
        
    def loadCharacterData(self, characterList):
        for characterName, aliasList in characterList:
            self.characters.append([characterName, aliasList])
            self.addAliasRow(characterName)
            
    def openNameDialog(self):
        dialog = NameDialog()
        if dialog.exec() == QDialog.Accepted:  
            name = dialog.getName()  
            return name
    
    def deleteCharacter(self, name, layout):
        i = next((i for i, character in enumerate(self.characters) if character[0] == name), -1)
        if i != -1:
            self.characters.pop(i)
            for i in reversed(range(layout.count())): 
                widget = layout.itemAt(i).widget()
                if widget is not None: 
                    widget.deleteLater()
            self.nameLayout.removeItem(layout)
        QMessageBox.information(self, "Remove Character", f"Removed {name}.")
    
    def editName(self, name):
        i = next((i for i, character in enumerate(self.characters) if character[0] == name), -1)
        if i != -1:
            characterEditDialog = speakerForm(self.characters[i])
            if characterEditDialog.exec() == QDialog.Accepted:  
                character = characterEditDialog.getCharacter()
                if character[0] != name:
                    self.updateCharacterName(name, character[0])
                self.characters[i] = character
        else:
            print("ERROR: Trying to edit character that doesn't exist") # TODO add actual error handling to this

    def updateCharacterName(self, old_name, name):
        i = next((i for i, layout in enumerate(self.nameLayout.children()) if layout.itemAt(0).widget().text() == old_name))
        layout = self.nameLayout.itemAt(i)
        
        label = layout.itemAt(0).widget()
        label.setText(name)
        label.setAccessibleName(f"Name: {name}")
        
        editButton = layout.itemAt(1).widget()
        editButton.clicked.disconnect()
        editButton.clicked.connect(lambda: self.editName(name))
        editButton.setAccessibleName(f"Edit {name} Button")
        
        deleteButton = layout.itemAt(2).widget()
        deleteButton.clicked.disconnect()
        deleteButton.clicked.connect(lambda: self.deleteCharacter(name, layout))

    def parseJSONToList(self):
        # load JSON file data into dict
        with open(self.characterFile, 'r') as file:
            self.characterJSON = json.load(file)

        # convert to list format for other functions
        inputList = [] # list that gets passed to LoadCharacterData()
        for speaker in self.characterJSON:
            characterName = speaker
            aliasList = []
            for alias in self.characterJSON[speaker]:
                newAlias = []
                newAlias.append(alias)
                tagList = ""
                for tag in self.characterJSON[speaker][alias]:
                    tagList += tag + ": "
                    tagList += str(self.characterJSON[speaker][alias][tag]) + ", "
                tagList = tagList[:len(tagList) - 2]
                newAlias.append(tagList)
                aliasList.append(newAlias)
            inputList.append([characterName, aliasList])
            
        return inputList

    def loadCharactersFromJSON(self, dirName):
        workingDir = os.path.dirname(os.path.abspath(__file__)) 
        filePath = os.path.join(workingDir+"\\" + dirName, 'characterlist.json')
        self.characterFile = filePath
        self.loadCharacterData(self.parseJSONToList())

    def saveListAsJSON(self):
        outputDict = {}
        for character in self.characters:
            # convert list of characters into individual character vars w/ some rudimentary error checking
            if character[0] != None:
                characterName = character[0]
            else:
                print("ERROR: Character object without associated name.")

            if character[1] != None:
                aliasList = character[1]
            else:
                print("ERROR: Character object has no aliases.")

            outputDict[characterName] = {}
        
            for i in range(len(aliasList)):
                # add alias name
                aliasName = aliasList[i][0]
                outputDict[characterName][aliasName] = {}

                # add alias tags from flattened data
                for tagStr in aliasList[i]:
                    if tagStr != aliasName:
                        tagStr = tagStr.replace(" ", "")
                        tagSep = tagStr.split(',')
                        for tag in tagSep:
                            tagParts = tag.split(':')
                            outputDict[characterName][aliasName][tagParts[0]] = tagParts[1]

        with open(self.characterFile, 'w') as file:
            json.dump(outputDict, file, indent=4)

    def onClose(self):
        self.close()
        self.saveListAsJSON()
        

class NameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter your name (Letters only)")

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        okButton.clicked.connect(self.confirm)
        cancelButton.clicked.connect(self.reject)  

        self.layout.addWidget(QLabel("Name:"))
        self.layout.addWidget(self.nameInput)
        self.layout.addWidget(okButton)
        self.layout.addWidget(cancelButton)

        self.setLayout(self.layout)
        self.setWindowTitle("Input Name")
        self.setModal(True)  

    def confirm(self):
        name = self.nameInput.text().strip()
        if not name.isalpha() or not name:
            QMessageBox.warning(self, "Invalid name", "Please enter a valid name. Only letters allowed.")
            return
        self.accept()  

    def getName(self):
        return self.nameInput.text().strip()  
      

if __name__ == "__main__":
    ExampleCharacterList = [
        ["Deckard", [["Deckard", "speed:1.0, pitch:1.0"], ["Rick",  "speed:1.0, pitch:1.1"]]],
        ["Ripley",  [["Ripley",  "speed:1.0, pitch:1.0"], ["Ellen", "speed:1.2, pitch:0.9"]]],
        ["Cooper",  [["Cooper",  "speed:1.0, pitch:1.0"], ["Joseph","speed:0.9, pitch:1.2"]]]
    ]
    app = QApplication(sys.argv)
    editor = CharacterManagerGUI()
    #editor.loadCharacterData(ExampleCharacterList)
    editor.loadCharactersFromJSON("Story_EX_DeleteLater")
    editor.resize(300, 400)
    editor.show()
    sys.exit(app.exec())
