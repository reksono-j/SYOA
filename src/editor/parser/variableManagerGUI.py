import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QScrollArea, QDialog, QLineEdit
)
from PySide6.QtGui import QRegExpValidator
from PySide6.QtCore import QRegExp
from speakerForm import *

class VariableManagerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # List Title
        self.label = QLabel("Variable List")
        self.label.setAccessibleName("Variable List")
        self.layout.addWidget(self.label)

        # Area where variables are
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)  
        self.scrollArea.setAccessibleName("Variable list")

        # Widget that holds a name
        self.nameContainer = QWidget()  
        self.nameLayout = QVBoxLayout(self.nameContainer)  
        self.scrollArea.setWidget(self.nameContainer)  
        self.layout.addWidget(self.scrollArea)

        # Add button
        self.addButton = QPushButton("Add Name")
        self.addButton.setAccessibleName("Add Name Button")
        self.addButton.clicked.connect(self.addVariable)
        self.layout.addWidget(self.addButton)

        # Close button
        self.closeButton = QPushButton("Close")
        self.closeButton.setAccessibleName("Close Button")
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)

        self.setLayout(self.layout)
        self.setWindowTitle("Variable Manager")

        self.variables = []
    
    def isPresent(self, name) -> bool:
        return name in self.variables

    def getVariables(self) -> list[str]:
        return self.variables
    
    def addVariable(self):
        name = self.openNameDialog()
        if not name:
            return
        self.variables.append(name)
        self.addAliasRow(name)

    def addAliasRow(self, name):
        nameLayout = QHBoxLayout()
        lineEdit = QLineEdit(self)
        
        noWhitespace = QRegExpValidator(QRegExp(r"\S+"))
        lineEdit.setValidator(noWhitespace)
        lineEdit.setPlaceholderText("Enter variable name here...")
        lineEdit.setText(name)
        # TODO: psbl + acc name
        
        toggleButton = QPushButton("Edit", self)
        toggleButton.setAccessibleName("Edit Variable Button")
        toggleButton.clicked.connect(lambda: lineEdit.setReadOnly(not lineEdit.isReadOnly()))
        
        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(lambda: self.deleteVariable(name, nameLayout))
        deleteButton.setAccessibleName("Delete Variable Button")
        
        nameLayout.addWidget(lineEdit)
        nameLayout.addWidget(toggleButton)
        nameLayout.addWidget(deleteButton)
        self.nameLayout.addLayout(nameLayout)  
        
    def loadVariableData(self, variableList):
        for variableName in variableList:
            self.variables.append(variableName)
            self.addAliasRow(variableName)
            
    def openNameDialog(self):
        dialog = NameDialog()
        if dialog.exec_() == QDialog.Accepted:  
            name = dialog.getName()  
            return name
    
    def deleteVariable(self, name, layout):
        i = next((i for i, variable in enumerate(self.variables) if variable == name), -1)
        if i != -1:
            self.variables.pop(i)
            for i in reversed(range(layout.count())): 
                widget = layout.itemAt(i).widget()
                if widget is not None: 
                    widget.deleteLater()
            self.nameLayout.removeItem(layout)
        QMessageBox.information(self, "Remove Variable", f"Removed {name}.")

class NameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter a name (alphanumeric))")

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
        if not (name[0].isalpha() and name.isalnum()) or not name:
            QMessageBox.warning(self, "Invalid name", "Please enter an alphanumeric name that starts with a letter.")
            return
        self.accept()  

    def getName(self):
        return self.nameInput.text().strip()  
      

if __name__ == "__main__":
    ExampleVariableList = [
        "Var1", "Var2"
    ]
    app = QApplication(sys.argv)
    editor = VariableManagerGUI()
    editor.loadVariableData(ExampleVariableList)
    editor.resize(300, 400)
    editor.show()
    sys.exit(app.exec_())
