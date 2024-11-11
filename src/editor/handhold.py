import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QTextEdit, QLabel

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

        #DO NOT DELETE THIS IS HOW TO READ TEXTEDIT
        #print(self.tbx.toPlainText())
        # DO NOT DELETE THIS IS HOW TO READ LINEEDIT
        # print(self.tbx.text())


        # Create a new button
        new_button = QPushButton("Dialogue")

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
        new_button = QPushButton("Split (in progress)")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+2

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.splf(new_button))
        new_button = QPushButton("Save (testing)")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+3

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)

        new_button.clicked.connect(self.OOO)
    def splf(self, button):
        label = QtWidgets.QLabel('SPLIT:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)
        deln = index
        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        label = QtWidgets.QLabel('List the split options:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        new_button = QPushButton("Add another split")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 2

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.addtbx(new_button))

        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 3

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 4

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        for i in range(4):
            item = self.groupBox.layout.takeAt(deln - 3)
            if item.widget():
                item.widget().deleteLater()
        new_button.clicked.connect(lambda: self.add(new_button))
        self.groupBox.setLayout(self.groupBox.layout)

    def talking(self, button):
        index = self.groupBox.layout.indexOf(button)
        deln = index


        label = QtWidgets.QLabel('DIALOGUE:')




        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        label = QtWidgets.QLabel('Name of the speaker:')
        index = index + 1
        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        tbx =  QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = index+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        label = QtWidgets.QLabel('What is the dialogue?')

        # Find the index of the clicked button in the layout
        index = index+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        tbx =  QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = index+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)
        new_button = QPushButton("DELETE DIALOGUE")

        # Find the index of the clicked button in the layout
        index = index + 1
        new_button.clicked.connect(lambda: self.DD(new_button))
        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index =index+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        '''self.groupBox.layout.removeWidget(button)
        button.deleteLater()'''
        for i in range(4):
            item = self.groupBox.layout.takeAt(deln - 3)
            if item.widget():
                item.widget().deleteLater()
        new_button.clicked.connect(lambda: self.add(new_button))
        self.groupBox.setLayout(self.groupBox.layout)


    def OOO(self):

        for i in range(self.groupBox.layout.count()):
            widget = self.groupBox.layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                print(widget.text())
                '''if widget.text() == "Name of the speaker:":
                    print(self.groupBox.layout.itemAt(i+1).widget().toPlainText())
                    print(self.groupBox.layout.itemAt(i + 3).widget().toPlainText())'''
            if isinstance(widget, QLineEdit):
                print(widget.text())
            if isinstance(widget, QTextEdit):
                print(widget.toPlainText())

    def DD(self, button):
        index = self.groupBox.layout.indexOf(button)
        for i in range(7):
            item = self.groupBox.layout.takeAt(index - 6)
            if item.widget():
                item.widget().deleteLater()

    def eee(self, button):
        label = QtWidgets.QLabel('CHOICE:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)
        deln = index

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)


        label = QtWidgets.QLabel('Type an existing event or a new one.')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 1


        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        new_button = QPushButton("Add another event")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 2

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.addtbx(new_button))

        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 3

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        new_button = QPushButton("DELETE CHOICES")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 4

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.delc(new_button,index))
        new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 5

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        for i in range(4):
            item = self.groupBox.layout.takeAt(deln - 3)
            if item.widget():
                item.widget().deleteLater()
        deleee = 0
        lol = 0
        for i in range(index-4,0,-1):
            widget = self.groupBox.layout.itemAt(i).widget()
            print(i)
            lol = lol + 1
            if isinstance(widget, QLabel):
                if widget.text() == "CHOICE:":
                    deleee = i

        new_button.clicked.connect(lambda: self.add(new_button))
        self.groupBox.setLayout(self.groupBox.layout)

    def delc(self, button, index):
        deleee = 0
        index = self.groupBox.layout.indexOf(button)
        lol = 0
        for i in range(index-1, 0, -1):
            widget = self.groupBox.layout.itemAt(i).widget()
            print(i)
            lol = lol + 1
            if isinstance(widget, QLabel):
                if widget.text() == "CHOICE:":
                    deleee = i
                    break
        for i in range(lol+1):
            item = self.groupBox.layout.takeAt(deleee)
            if item.widget():
                item.widget().deleteLater()

    def addtbx(self, button):
        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index-1, tbx)

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
