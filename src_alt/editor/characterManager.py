import json
import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QScrollArea, QDialog, QLineEdit,
    QSizePolicy, QGridLayout
)
class Character:
    def __init__(self, name):
        self.name = name
        self.aliases = {name: None}  # Character's name is the default alias

    def addAlias(self, alias, displayName=None):
        if alias not in self.aliases:
            self.aliases[alias] = displayName  # Store display name or None

    def removeAlias(self, alias):
        if alias in self.aliases and alias != self.name:  # Can't remove the character's name
            del self.aliases[alias]

    def updateAlias(self, alias, newDisplayName):
        if alias in self.aliases:
            self.aliases[alias] = newDisplayName

    def renameCharacter(self, newName):
        if newName != self.name:
            self.aliases[newName] = self.aliases.pop(self.name) 
            self.name = newName

    def getDisplayName(self, alias):
        return alias if self.aliases[alias] is None else self.aliases[alias]

    def getName(self):
        return self.name
    
    def getAliases(self):
        return self.aliases

class CharacterManager:
    def __init__(self):
        self.characters = {}

    def addCharacter(self, character):
        if character.name not in self.characters:
            self.characters[character.name] = character

    def removeCharacter(self, characterName):
        if characterName in self.characters:
            del self.characters[characterName]
            
    def getCharacters(self):
        return self.characters
    
    def getCharacter(self, characterName):
        return self.characters.get(characterName)

    def listCharacters(self):
        return self.characters.keys()

    def saveToFile(self, path):
        with open(path, 'w') as f:
            json.dump({name: character.getAliases() for name, character in self.characters.items()}, f)

    def loadFromFile(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                characterData = json.load(f)
                for name, aliases in characterData.items():
                    character = Character(name)
                    for alias, displayName in aliases.items():
                        character.addAlias(alias, displayName)
                    self.addCharacter(character)



class CharacterForm(QDialog):
    def __init__(self, char: Character):
        super().__init__()
        self.layout = QGridLayout()
        self.character = char
        self.initialData = None
        
        # Speaker name bar
        self.speakerLabel = QLabel("Speaker")
        self.speakerLabel.setAccessibleName("Speaker")

        self.speakerName = QLineEdit(char.getName())
        self.speakerName.setAccessibleName("Name Field")
        self.changeButton = QPushButton("Change Name")
        self.changeButton.setAccessibleName("Toggle Name Change")
        
        self.speakerLabel.setBuddy(self.speakerName)
        self.speakerName.setReadOnly(True)
        self.changeButton.clicked.connect(self.toggleReadOnly)
        
        self.layout.addWidget(self.speakerLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.speakerName, 0, 1, 1, 1) 
        self.layout.addWidget(self.changeButton, 0, 2, 1, 1)
        
        self.aliases = []
        self.displayNames = []

        # Add and confirm buttons
        self.confirmButton = QPushButton("Confirm")
        self.confirmButton.setAccessibleName("Confirm Button")
        self.confirmButton.clicked.connect(self.confirmCharacter)

        self.addButton = QPushButton("Add")
        self.addButton.setAccessibleName("Add Alias Button")
        self.addButton.clicked.connect(self.addAlias)


        self.layout.setColumnStretch(0, 1)           
        self.layout.setColumnStretch(1, 3)
        self.setLayout(self.layout)

        self.rowCount = 1
        
        # Adds rows to enter aliases and repositions confirm and add buttons
        # TODO: Make this so that it can construct pre-filled rows
        self.loadAliasData(char)

    def addAlias(self):
        self.addAliasWidgetRow("", "")
        self.repositionButtons()
        
    def addAliasWidgetRow(self, name, tags):
        aliasLabel = QLabel(f"Alias {len(self.aliases) + 1}")
        aliasInput = QLineEdit()
        aliasInput.setText(name)
        
        # TODO Figure out how to retroactively update the accessible names when lineedit changes
        aliasLabel.setBuddy(aliasInput)
        aliasSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        aliasInput.setSizePolicy(aliasSizePolicy)
        
        displayNameLabel = QLabel(f"DisplayN {len(self.displayNames) + 1}")
        displayNameInput = QLineEdit()
        displayNameInput.setText(tags)
        
        # TODO: Accessible name
        displayNameLabel.setBuddy(displayNameInput)
        displayNameSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        displayNameInput.setSizePolicy(displayNameSizePolicy)
        
        self.layout.addWidget(aliasLabel, self.rowCount, 0)
        self.layout.addWidget(aliasInput, self.rowCount + 1, 0)
        self.layout.addWidget(displayNameLabel, self.rowCount, 1)
        self.layout.addWidget(displayNameInput, self.rowCount + 1, 1, 1 , 2)

        self.aliases.append(aliasInput)
        self.displayNames.append(displayNameInput)

        self.rowCount += 2
    
    def repositionButtons(self):
        self.layout.addWidget(self.addButton, self.rowCount, 0, 1, 3)
        self.layout.addWidget(self.confirmButton, self.rowCount + 1, 0, 1, 3)   
    
    def loadAliases(self):
        for alias, displayName in self.character.getAliases():
            self.addAliasWidgetRow(alias, displayName)
          
        self.repositionButtons()
      
    def toggleReadOnly(self):
        self.speakerName.setReadOnly(not self.speakerName.isReadOnly())

    def saveCharacter(self):
        if self.speakerLabel != self.character.getName():
            self.character.renameCharacter(self.speakerLabel.text())
        for i in range(len(self.displayNames)):
            alias = self.aliases[i]
            if alias != "":
                if alias in self.character.aliases:
                    self.character.updateAlias(alias, self.displayNames[i])
                else:
                    self.character.addAlias(alias, self.displayNames[i])
        self.accept()
    
    def getCharacter(self):
        return self.character


class CharacterManagerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.characterManager = CharacterManager()
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
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)

        self.setLayout(self.layout)
        self.setWindowTitle("Character Manager")

        self.characters = []
        
        self.loadCharacters()
    
    def addCharacter(self):
        name = self.openNameDialog()
        if not name:
            return
        self.characters.append([name, {}])
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
        
    def loadCharacters(self):
        charNames = self.characterManager.listCharacters()
        for name in charNames:
            character = self.characterManager.getCharacter(name)
            self.characters.append([character.getName(), character.getAliases()])
            self.addAliasRow(name)
        self.initialData = self.characters
            
    def openNameDialog(self):
        dialog = NameDialog()
        if dialog.exec_() == QDialog.Accepted:  
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
            characterEditDialog = CharacterForm(self.characters[i])
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
    
    def saveAll(self):
        pass

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
    app = QApplication(sys.argv)
    editor = CharacterManagerGUI()
    editor.loadCharacters()
    editor.resize(300, 400)
    editor.show()
    sys.exit(app.exec_())
