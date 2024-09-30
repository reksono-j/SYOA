import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QSizePolicy


class speakerForm(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.layout = QGridLayout()

        self.speakerLabel = QLabel("Speaker")
        self.speakerLabel.setAccessibleName("Speaker")
        self.speakerName = QLineEdit(name)
        self.speakerName.setAccessibleName("Name")
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

        self.saveButton = QPushButton("Save")
        self.saveButton.setAccessibleName("Save")
        self.saveButton.clicked.connect(self.saveCharacter)

        self.addButton = QPushButton("Add")
        self.addButton.setAccessibleName("Add Alias")
        self.addButton.clicked.connect(self.addAliasRow)

        self.layout.setColumnStretch(0, 1)           
        self.layout.setColumnStretch(1, 3)
        self.setLayout(self.layout)

        self.rowCount = 1
        self.addAliasRow()

    def addAliasRow(self):
        aliasLabel = QLabel(f"Alias {len(self.aliases) + 1}")
        aliasInput = QLineEdit()
        
        # TODO Figure out how to retroactively update the accessible names when lineedit changes
        
        aliasLabel.setBuddy(aliasInput)
        aliasSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        aliasInput.setSizePolicy(aliasSizePolicy)

        tagLabel = QLabel(f"Speaker Tags {len(self.tags) + 1}")
        tagInput = QLineEdit()
        # TODO: Accessible names
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

        self.layout.addWidget(self.addButton, self.rowCount, 0, 1, 3)
        self.layout.addWidget(self.saveButton, self.rowCount + 1, 0, 1, 3)   
    
    def toggleReadOnly(self):
      self.speakerName.setReadOnly(not self.speakerName.isReadOnly())

    def saveCharacter(self):
      pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = speakerForm("test")
    window.show()
    sys.exit(app.exec_())
