import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QScrollArea, QDialog, QLineEdit
)
from Speakerform import *

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
        self.closeButton.clicked.connect(self.close)
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
            characterEditDialog = Speakerform(self.characters[i])
            if characterEditDialog.exec_() == QDialog.Accepted:  
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
        ["Deckard", [["Deckard", "Decky"], ["Rick",  "Decks"]]],
        ["Ripley",  [["Ripley",  "Ripley"], ["Ellen", "Rip"]]],
        ["Cooper",  [["Cooper",  "Coop"], ["Joseph",""]]]
    ]
    app = QApplication(sys.argv)
    editor = CharacterManagerGUI()
    editor.loadCharacterData(ExampleCharacterList)
    editor.resize(300, 400)
    editor.show()
    sys.exit(app.exec_())
