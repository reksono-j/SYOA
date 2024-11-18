import os
import json
from PySide6.QtWidgets import (
    QApplication, QDialog, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QSizePolicy, QWidget, QVBoxLayout, 
    QHBoxLayout, QMessageBox, QScrollArea
)
from src_alt.editor.singleton import Singleton
from src_alt.editor.projectManager import ProjectManager

# Character class with aliases management
class Character:
    def __init__(self, name):
        self.name = name
        self.aliases = {name: None}  # Character's name is the default alias

    # TODO: Add Voice model aption
    
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

    # TODO
    def getDisplayName(self, alias):
        return alias if self.aliases[alias] is None else self.aliases[alias]

    def getData(self, alias):
        if alias in self.aliases: # TODO: Replace str "" with {}
            return "" if self.aliases[alias] is None else self.aliases[alias] 
        else:
            return ""
        
    
    def getName(self):
        return self.name
    
    def getAliases(self):
        return self.aliases

class CharacterManager(metaclass=Singleton):
    def __init__(self):
        self.projectManager = ProjectManager()
        self.characters = {str: Character}
        
        self.projectManager.changedProject.connect(self.updatePath)
        self.updatePath()

    def updatePath(self):
        path = self.projectManager.getCurrentFilePath()
        path = os.path.join(path, 'characters.json')  
        self.path = path 
        if self.path:
            self.loadCharacters()
            
    def addCharacter(self, character:Character):
        if character.name not in self.characters:
            self.characters[character.name] = character

    def removeCharacter(self, characterName):
        if characterName in self.characters:
            del self.characters[characterName]
            
    def getCharacters(self):
        return self.characters
    
    def getAliasInfo(self, alias: str):
        for name, character in self.characters.items():
            aliases = character.getAliases()
            if alias in aliases:
                return character.getData(alias)
        return ""
    
    # This takes a character name and replaces the character data of that character
    def updateCharacter(self, currentName, updatedCharacter):
        if currentName in self.characters:
            if updatedCharacter.getName() != currentName:
                self.characters[updatedCharacter.getName()] = self.characters.pop(currentName)
            else:
                self.characters[currentName] = updatedCharacter
    
    def getCharacter(self, characterName):
        return self.characters.get(characterName)

    def listCharacters(self):
        return self.characters.keys()

    def saveCharacters(self):
        with open(self.path, 'w') as f:
            json.dump({name: character.getAliases() for name, character in self.characters.items()}, f)

    def loadCharacters(self):
        self.characters.clear()
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                characterData = json.load(f)
                for name, aliases in characterData.items():
                    character = Character(name)
                    for alias, displayName in aliases.items():
                        character.addAlias(alias, displayName)
                    self.addCharacter(character)

# CharacterManagerDialog for adding, editing, and listing characters
class CharacterManagerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 800)
        
        self.layout = QVBoxLayout()

        # Title
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
        self.addButton.setAccessibleName("Add Name")
        self.addButton.clicked.connect(self.addCharacter)
        self.layout.addWidget(self.addButton)

        # Close button
        self.closeButton = QPushButton("Close")
        self.closeButton.setAccessibleName("Close")
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)

        self.setLayout(self.layout)
        self.setWindowTitle("Character Manager")

        self.characterManager = CharacterManager()
        self.updateCharacterList()

    def addCharacter(self):
        name = self.openNameDialog()
        if not name:
            return
        if self.characterManager.getCharacter(name) is None:
            character = Character(name)
            self.characterManager.addCharacter(character)
            self.addAliasRow(character)
            self.characterManager.saveCharacters()
    
    def addAliasRow(self, character):
        name = character.getName()
        nameLayout = QHBoxLayout()
        nameLabel = QLabel(name)
        nameLabel.setAccessibleName(f"Name: {name}")  
        editButton = QPushButton("Edit")
        editButton.setAccessibleName(f"Edit {name} Button")  
        editButton.clicked.connect(lambda: self.editCharacter(character))
        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(lambda: self.deleteCharacter(character, nameLayout))
        deleteButton.setAccessibleName(f"Delete {name} Button")

        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(editButton)
        nameLayout.addWidget(deleteButton)
        self.nameLayout.addLayout(nameLayout)
        
    def openNameDialog(self):
        dialog = NameDialog()
        if dialog.exec_() == QDialog.Accepted:
            return dialog.getName()

    def updateCharacterList(self):
        for characterName in self.characterManager.listCharacters():
            character = self.characterManager.getCharacter(characterName)
            self.addAliasRow(character)

    def deleteCharacter(self, character, layout):
        self.characterManager.removeCharacter(character.getName())
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.nameLayout.removeItem(layout)
        self.characterManager.saveCharacters()
        QMessageBox.information(self, "Remove Character", f"Removed {character.getName()}.")

    def editCharacter(self, character):
        dialog = CharacterForm(character)
        if dialog.exec_() == QDialog.Accepted:
            updatedCharacter = dialog.getCharacter()
            self.characterManager.updateCharacter(character.getName(), updatedCharacter)
            self.characterManager.saveCharacters()

# Name Dialog to input a new character's name
class NameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter character name (Letters only)")

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


class CharacterForm(QDialog):
    def __init__(self, character):
        super().__init__()
        self.layout = QGridLayout()
        
        # Speaker name bar
        self.speakerLabel = QLabel("Speaker")
        self.speakerLabel.setAccessibleName("Speaker")

        self.speakerName = QLineEdit(character.getName())
        self.speakerName.setAccessibleName("Name Field")
        
        self.speakerLabel.setBuddy(self.speakerName)
        
        self.layout.addWidget(self.speakerLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.speakerName, 0, 1, 1, 1)
        
        # Add and confirm buttons
        self.confirmButton = QPushButton("Confirm")
        self.confirmButton.setAccessibleName("Confirm Button")
        self.confirmButton.clicked.connect(self.confirmCharacter)

        self.addButton = QPushButton("Add")
        self.addButton.setAccessibleName("Add Alias Button")
        self.addButton.clicked.connect(self.addAlias)

        self.aliasInputs = []
        self.nameInputs = []
        
        self.layout.setColumnStretch(0, 1)           
        self.layout.setColumnStretch(1, 3)
        self.setLayout(self.layout)

        self.rowCount = len(character.getAliases())
        
        # Adds rows to enter aliases and repositions confirm and add buttons
        # TODO: Make this so that it can construct pre-filled rows
        self.loadAliasData(character.getAliases())

    def addAlias(self):
        self.addAliasWidgetRow("", "")
        self.repositionButtons()
        
    def addAliasWidgetRow(self, alias, displayName):
        aliasLabel = QLabel(f"Alias {len(self.aliasInputs) + 1}")
        
        aliasInput = QLineEdit()
        aliasInput.setText(alias)
        # TODO Figure out how to retroactively update the accessible names when lineedit changes
        aliasLabel.setBuddy(aliasInput)
        aliasSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        aliasInput.setSizePolicy(aliasSizePolicy)
        self.aliasInputs.append(aliasInput)
         
        nameLabel = QLabel(f"Display Name {len(self.nameInputs) + 1}")
        nameInput = QLineEdit() # TODO: replace with drop down that shows the available models
        nameInput.setText(displayName)
        # TODO: Accessible name
        nameLabel.setBuddy(nameInput)
        nameSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nameInput.setSizePolicy(nameSizePolicy)
        self.nameInputs.append(nameInput)
        
        self.layout.addWidget(aliasLabel, self.rowCount, 0)
        self.layout.addWidget(aliasInput, self.rowCount + 1, 0)
        self.layout.addWidget(nameLabel, self.rowCount, 1)
        self.layout.addWidget(nameInput, self.rowCount + 1, 1, 1 , 2)

        self.rowCount += 2
    
    def repositionButtons(self):
        self.layout.addWidget(self.addButton, self.rowCount, 0, 1, 3)
        self.layout.addWidget(self.confirmButton, self.rowCount + 1, 0, 1, 3)   
    
    def loadAliasData(self, aliases):
        if aliases:
            for alias, name in aliases.items():
                self.addAliasWidgetRow(alias, name)
        else:
            self.addAlias()
          
        self.repositionButtons()

    def confirmCharacter(self):
        character = Character(self.speakerName.text())
        for i in range(len(self.aliasInputs)):
            character.addAlias(self.aliasInputs[i].text(), self.nameInputs[i].text())
        self.character = character
        self.accept()
    
    def getCharacter(self):
        return self.character