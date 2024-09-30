import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QScrollArea, QDialog, QLineEdit
)
from speakerForm import *

class CharacterManager(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel("Character List")
        self.label.setAccessibleName("Character List")
        self.layout.addWidget(self.label)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)  
        self.scrollArea.setAccessibleName("Character list")

        self.nameContainer = QWidget()  
        self.nameLayout = QVBoxLayout(self.nameContainer)  
        self.scrollArea.setWidget(self.nameContainer)  
        self.layout.addWidget(self.scrollArea)

        self.addButton = QPushButton("Add Name")
        self.addButton.setAccessibleName("Add Name Button")
        self.addButton.clicked.connect(self.addCharacter)
        self.layout.addWidget(self.addButton)

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
        self.characters.append(name)
        
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

    def openNameDialog(self):
        dialog = NameDialog()
        if dialog.exec_() == QDialog.Accepted:  
            name = dialog.getName()  
            return name
    
    def deleteCharacter(self, name, layout):
        if name in self.characters:
            self.characters.remove(name)
            for i in reversed(range(layout.count())): 
                widget = layout.itemAt(i).widget()
                if widget is not None: 
                    widget.deleteLater()
            self.nameLayout.removeItem(layout)
        QMessageBox.information(self, "Remove Character", f"Removed {name}.")
    
    def editName(self, name):
        self.characterMenu = speakerForm(name)
        self.characterMenu.show()
     

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
    editor = CharacterManager()
    editor.resize(300, 400)
    editor.show()
    sys.exit(app.exec_())
