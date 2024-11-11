import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class HandHoldMenu(QtWidgets.QScrollArea):
    def __init__(self, HandHoldManager, parent):
        super(HandHoldMenu, self).__init__(parent)
        self.parent = parent
        self.HandHoldManager = HandHoldManager
        self.initParameters()
        self.initUI()
      
    def initParameters(self):
        self.opened = False  

    # action method
    def initUI(self):
        self.groupBox = QtWidgets.QGroupBox("Hand Hold")
        self.setWidget(self.groupBox)
        self.setWidgetResizable(True)
        self.groupBox.layout = QtWidgets.QVBoxLayout()
        # printing pressed
        print("pressed")
        self.count = 100
        title = True

        self.label = QtWidgets.QLabel('Give a title for this event:', self)
        self.groupBox.layout.addWidget(self.label)
        self.tbx = QtWidgets.QTextEdit(self)
        self.tbx.setAccessibleName("Event title text box. ")
        self.tbx.setAccessibleDescription("Insert an event title here.")
        self.groupBox.layout.addWidget(self.tbx)
        self.button = QPushButton("Add")
        self.groupBox.layout.addWidget(self.button)
        self.button.clicked.connect(lambda: self.add(self.button))

        self.groupBox.setLayout(self.groupBox.layout)


    def add(self, button):

        # Create a new button
        new_button = QPushButton("Dialodue")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.talking(new_button))
        new_button = QPushButton("Choice")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.eee(new_button))
        new_button = QPushButton("Split")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+2

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        button.clicked.connect(lambda: self.add(new_button))
        new_button = QPushButton("O4")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+3

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.add(new_button))



    def talking(self, button):
        label = QtWidgets.QLabel('Name of the speaker:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)


        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        tbx =  QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        label = QtWidgets.QLabel('What is the dialogue?')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+2

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        tbx =  QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+3

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)
        new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+4

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.add(new_button))
        self.groupBox.setLayout(self.groupBox.layout)



    def eee(self, button):

        label = QtWidgets.QLabel('Type an existing event or a new one.')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        new_button = QPushButton("Add another event")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.addtbx(new_button))

        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 2

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 3

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.add(new_button))
        self.groupBox.setLayout(self.groupBox.layout)

    def addtbx(self, button):
        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, tbx)

    def toggleUI(self):
        if (self.opened):
            self.close()
            self.opened = False
        else:
            self.show()
            self.opened = True

class HandHoldManager:
    def __init__(self, window) -> None:
        self.window = window
        self.menu = HandHoldMenu(self, window)

    def menuToggle(self):
        self.menu.toggleUI()
