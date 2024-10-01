import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QSizePolicy


class speakerForm(QDialog):
    def __init__(self, character):
        super().__init__()
        self.layout = QGridLayout()
        
        # Speaker name bar
        self.speakerLabel = QLabel("Speaker")
        self.speakerLabel.setAccessibleName("Speaker")

        self.speakerName = QLineEdit(character[0])
        self.speakerName.setAccessibleName("Name Field")
        self.changeButton = QPushButton("Change Name")
        self.changeButton.setAccessibleName("Toggle Name Change") # TODO: Think of better description for this
        
        self.speakerLabel.setBuddy(self.speakerName)
        self.speakerName.setReadOnly(True)
        self.changeButton.clicked.connect(self.toggleReadOnly)
        
        self.layout.addWidget(self.speakerLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.speakerName, 0, 1, 1, 1) 
        self.layout.addWidget(self.changeButton, 0, 2, 1, 1)
        
        self.aliases = []
        self.tags = []

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
        self.loadAliasData(character[1])

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
        
        tagLabel = QLabel(f"Speaker Tags {len(self.tags) + 1}")
        tagInput = QLineEdit()
        tagInput.setText(tags)
        # TODO: Accessible name
        tagLabel.setBuddy(tagInput)
        tagSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        tagInput.setSizePolicy(tagSizePolicy)
        
        self.layout.addWidget(aliasLabel, self.rowCount, 0)
        self.layout.addWidget(aliasInput, self.rowCount + 1, 0)
        self.layout.addWidget(tagLabel, self.rowCount, 1)
        self.layout.addWidget(tagInput, self.rowCount + 1, 1, 1 , 2)

        self.aliases.append(aliasInput)
        self.tags.append(tagInput)

        self.rowCount += 2
    
    def repositionButtons(self):
        self.layout.addWidget(self.addButton, self.rowCount, 0, 1, 3)
        self.layout.addWidget(self.confirmButton, self.rowCount + 1, 0, 1, 3)   
    
    def loadAliasData(self, aliasList):
        if aliasList:
            for character in aliasList:
                self.addAliasWidgetRow(character[0], character[1])
        else:
            self.addAlias()
          
        self.repositionButtons()
      
    def toggleReadOnly(self):
        self.speakerName.setReadOnly(not self.speakerName.isReadOnly())

    def confirmCharacter(self):
        aliasList = []
        for i in range(len(self.tags)):
            aliasList.append([self.aliases[i].text(), self.tags[i].text()])
        self.character = [self.speakerName.text(), aliasList]
        self.accept()
    
    def getCharacter(self):
        return self.character

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = speakerForm(["test",[]])
    window.show()
    sys.exit(app.exec_())
