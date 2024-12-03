from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QMenu,
    QInputDialog, QDialog, QFormLayout
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal
from src.editor.variableManager import EditorVariableManager

class AddVariableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Variable')
        self.layout = QFormLayout(self)
        
        self.variableNameInput = QLineEdit(self)
        self.variableNameInput.setAccessibleName("Name field")
        self.variableValueInput = QLineEdit(self)
        self.variableValueInput.setAccessibleName("Value field")
        
        self.layout.addRow('Name:', self.variableNameInput)
        self.layout.addRow('Initial Value (Integer):', self.variableValueInput)
        
        self.addButton = QPushButton('Add', self)
        self.addButton.setAccessibleName("Add")
        self.addButton.clicked.connect(self.accept)
        self.layout.addWidget(self.addButton)

    def getInputs(self):
        name = self.variableNameInput.text()
        valueText = self.variableValueInput.text()
        return name, valueText

class VariableManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 600, 400)
        self.setContentsMargins(0, 0, 0, 0)
        
        layout = QVBoxLayout(self)
        self.variableManagerGUI = EditorVariableManagerGUI()
        self.variableManagerGUI.closeGUI.connect(self.close)
        layout.addWidget(self.variableManagerGUI)
        self.setLayout(layout)

class EditorVariableManagerGUI(QWidget):
    closeGUI = Signal()
    
    def __init__(self):
        super().__init__()

        self.vm = EditorVariableManager()  
        self.vm.loadVariables()  
        self.lastEditedVariable = None  
        self.initUI()
        self.listVariables()  

    def initUI(self):
        self.setWindowTitle('Variable Manager')
        self.setGeometry(100, 100, 500, 400)
        layout = QVBoxLayout()

        self.addButton = QPushButton('Add Variable', self)
        self.addButton.clicked.connect(self.openAddVariableDialog)
        self.addButton.setAccessibleName('Add Variable Button')
        layout.addWidget(self.addButton)

        self.variableList = QListWidget(self)
        self.variableList.itemDoubleClicked.connect(self.showVariableOptions)
        self.variableList.setAccessibleName('List of Variables')
        self.variableList.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        layout.addWidget(self.variableList)

        
        self.exitButton = QPushButton('Exit', self)
        self.exitButton.clicked.connect(self.closeApp) 
        layout.addWidget(self.exitButton)

        self.setLayout(layout)
        self.listVariables() 
    
    def closeApp(self):
        self.closeGUI.emit()
        self.close()

    def openAddVariableDialog(self):
        dialog = AddVariableDialog(self)
        if dialog.exec() == QDialog.Accepted:
            name, valueText = dialog.getInputs()
            self.addVariable(name, valueText)

    def addVariable(self, name, valueText):
        if name:
            try:
                value = int(valueText)
                if name.lower() in self.vm.Variables:
                    self.showError(f"The variable '{name}' already exists. Please choose a different name.")
                    return  
                if self.vm.setVariable(name, value):
                    self.listVariables()
                else:
                    self.showError("Invalid variable name or value must be an integer.")
            except ValueError:
                self.showError("Value must be an integer.")


    def showVariableOptions(self, item):
        variableName = item.text().split(':')[0]
        menu = QMenu(self)

        renameAction = QAction(f'Rename "{variableName}"', self)
        renameAction.triggered.connect(lambda: self.renameVariable(variableName))
        menu.addAction(renameAction)

        changeValueAction = QAction(f'Change Value of "{variableName}"', self)
        changeValueAction.triggered.connect(lambda: self.changeVariableValue(variableName))
        menu.addAction(changeValueAction)

        deleteAction = QAction(f'Delete "{variableName}"', self)
        deleteAction.triggered.connect(lambda: self.deleteVariable(variableName))
        menu.addAction(deleteAction)

        itemRect = self.variableList.visualItemRect(item)  
        globalPos = self.variableList.mapToGlobal(itemRect.topLeft())  

        menu.exec(globalPos)  

    def renameVariable(self, oldName):
        newName, ok = QInputDialog.getText(self, 'Rename Variable', 'New Variable Name:')
        if ok and newName:
            if self.vm.isValidName(newName) and newName.lower() not in self.vm.Variables:
                self.vm.renameVariable(oldName, newName)
                self.lastEditedVariable = newName  
                self.listVariables()
            else:
                self.showError("Invalid name for renaming or name already exists.")

    def changeVariableValue(self, name):
        newValueText, ok = QInputDialog.getText(self, 'Change Variable Value', 'New Value (Integer):')
        if ok and newValueText:
            try:
                newValue = int(newValueText)
                if self.vm.setVariable(name, newValue):
                    self.lastEditedVariable = name  
                    self.listVariables()
                else:
                    self.showError("Invalid value. Value must be an integer.")
            except ValueError:
                self.showError("Value must be an integer.")

    def deleteVariable(self, name):
        self.vm.deleteVariable(name)
        self.listVariables()

    def listVariables(self):
        self.variableList.clear()
        
        for name, value in self.vm.listVariables():
            self.variableList.addItem(f"{name}: {value}")
        
        if self.lastEditedVariable:
            for i in range(self.variableList.count()):
                if self.variableList.item(i).text().startswith(self.lastEditedVariable):
                    self.variableList.setCurrentRow(i)  
                    self.variableList.setFocus()  
                    return  
        
        if self.variableList.count() > 0:
            self.variableList.setCurrentRow(0)  
            self.variableList.setFocus()  

    def showError(self, message):
        QMessageBox.critical(self, "Error", message)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            if self.focusWidget() == self.addButton:
                self.addButton.clicked.emit()
            elif self.focusWidget() == self.exitButton:
                 self.exitButton.clicked.emit()
            else:
                currentItem = self.variableList.currentItem()
                if currentItem:
                    self.showVariableOptions(currentItem)

        elif event.key() == Qt.Key.Key_Delete:
            currentItem = self.variableList.currentItem()
            if currentItem:
                self.deleteVariable(currentItem.text().split(':')[0])

        elif event.key() == Qt.Key.Key_Escape:
            self.exitButton.setFocus()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = EditorVariableManagerGUI()
    window.show()
    sys.exit(app.exec())

