from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit, QTextEdit, QLabel

class HandHoldMenu(QtWidgets.QScrollArea):
    def __init__(self, HandHoldManager, parent=None):
        super(HandHoldMenu, self).__init__(parent)
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
        self.groupBox.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # printing pressed
        # print("pressed")
        self.saver = False
        self.saver2 = False
        self.button33 = QPushButton("Reset")

        self.groupBox.layout.addWidget(self.button33)
        self.button33.clicked.connect(lambda: self.res(self.button33))

        self.button = QPushButton("Save")

        self.groupBox.layout.addWidget(self.button)
        self.button.clicked.connect(lambda: self.save(self.button))

        self.button12 = QPushButton("Add")

        self.groupBox.layout.addWidget(self.button12)
        self.button12.clicked.connect(lambda: self.add(self.button12))

        self.button3 = QPushButton("Save")

        self.groupBox.layout.addWidget(self.button3)
        self.button3.clicked.connect(lambda: self.save(self.button3))

        self.button34 = QPushButton("Reset")

        self.groupBox.layout.addWidget(self.button34)
        self.button34.clicked.connect(lambda: self.res(self.button34))
        self.groupBox.setLayout(self.groupBox.layout)

    def res(self,button):
        for i in range(self.groupBox.layout.count()):
            item = self.groupBox.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.saver = False
        self.saver2 = False
        self.button33 = QPushButton("Reset")

        self.groupBox.layout.addWidget(self.button33)
        self.button33.clicked.connect(lambda: self.res(self.button33))

        self.button = QPushButton("Save")

        self.groupBox.layout.addWidget(self.button)
        self.button.clicked.connect(lambda: self.save(self.button))

        self.button12 = QPushButton("Add")

        self.groupBox.layout.addWidget(self.button12)
        self.button12.clicked.connect(lambda: self.add(self.button12))

        self.button3 = QPushButton("Save")

        self.groupBox.layout.addWidget(self.button3)
        self.button3.clicked.connect(lambda: self.save(self.button3))

        self.button34 = QPushButton("Reset")

        self.groupBox.layout.addWidget(self.button34)
        self.button34.clicked.connect(lambda: self.res(self.button34))
        self.groupBox.setLayout(self.groupBox.layout)

    def save(self, button):
        final_string = ""
        for i in range(self.groupBox.layout.count()):
            widget = self.groupBox.layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                #print(widget.text())
                # '''if widget.text() == "Name of the speaker:":
                #     print(self.groupBox.layout.itemAt(i+1).widget().toPlainText())
                #     print(self.groupBox.layout.itemAt(i + 3).widget().toPlainText())'''
                if widget.text() == "Name of the speaker:":
                    final_string = final_string + self.groupBox.layout.itemAt(i+1).widget().toPlainText() + " : " + self.groupBox.layout.itemAt(i+3).widget().toPlainText() + "\n"
                if widget.text()[:13] == "END OF CHOICE":
                    final_string = final_string + "END" + "\n"
                if widget.text() == "Name of Choice:":
                    final_string = final_string + "CHOICE " + self.groupBox.layout.itemAt(
                        i + 1).widget().toPlainText() + "\n"
                if widget.text()[:7] == "Branch ":
                    final_string = final_string + "BRANCH " + self.groupBox.layout.itemAt(i+1).widget().toPlainText() + "\n"
                if widget.text() == "Name of the variable:":
                    var1 = self.groupBox.layout.itemAt(i+1).widget().toPlainText()
                    sett = self.groupBox.layout.itemAt(i+3).widget().toPlainText()
                    if sett == "+":
                        sett = "ADD"
                    if sett == "-":
                        sett = "SUB"
                    else:
                        sett = "SET"
                    var2 = self.groupBox.layout.itemAt(i+5).widget().toPlainText()
                    final_string = final_string + "MODIFY " + var1 + " " + sett + " " + var2 + "\n"
                if widget.text() == "Variable Name:":
                    var1 = self.groupBox.layout.itemAt(i+1).widget().toPlainText()
                    sett = self.groupBox.layout.itemAt(i+3).widget().toPlainText()
                    if sett == ">":
                        sett = "MORE"
                    if sett == "<":
                        sett = "LESS"
                    if sett == "<=":
                        sett = "LTE"
                    if sett == ">=":
                        sett = "MTE"
                    else:
                        sett = "EQ"
                    var2 = self.groupBox.layout.itemAt(i+5).widget().toPlainText()
                    final_string = final_string + "IF " + var1 + " " + sett + " " + var2 + "\n"
                if widget.text() == "END OF ELSE CONDITION AND CONDITIONAL":
                    final_string = final_string + "END" + "\n"
                if widget.text() == "ELSE:":
                    final_string = final_string + "ELSE" + "\n"

            # if isinstance(widget, QLineEdit):
            #     print(widget.text())
            # if isinstance(widget, QTextEdit):
            #     print(widget.toPlainText())

        # print(final_string)
        index = self.groupBox.layout.indexOf(button)
        if index < 4:

            if self.saver:
                item = self.groupBox.layout.takeAt(index-1)
                if item.widget():
                    item.widget().deleteLater()
                item = self.groupBox.layout.takeAt(index - 2)
                if item.widget():
                    item.widget().deleteLater()
                index = index - 2

            self.saver = True
            QApplication.clipboard().setText(final_string)
            label = QtWidgets.QLabel('The code is automatically copied. Hit Control V to paste into the IDE')
            index = index - 1
            # Insert the new button after the clicked button
            self.groupBox.layout.insertWidget(index + 1, label)
            tbx = QtWidgets.QTextEdit(self)
            tbx.setPlainText(final_string)


            # Find the index of the clicked button in the layout
            index = index + 1

            # Insert the new button after the clicked button
            self.groupBox.layout.insertWidget(index + 1, tbx)
        else:

            if self.saver2:
                item = self.groupBox.layout.takeAt(index+1)
                if item.widget():
                    item.widget().deleteLater()
                item = self.groupBox.layout.takeAt(index + 1)
                if item.widget():
                    item.widget().deleteLater()
            QApplication.clipboard().setText(final_string)
            label = QtWidgets.QLabel('The code is automatically copied. Hit Control V to paste into the IDE')

            # Insert the new button after the clicked button
            self.groupBox.layout.insertWidget(index + 1, label)
            self.saver2 = True
            index = index + 1
            tbx = QtWidgets.QTextEdit(self)
            tbx.setPlainText(final_string)


            # Insert the new button after the clicked button
            self.groupBox.layout.insertWidget(index + 1, tbx)
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
        new_button = QPushButton("End of Scene Branches")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.eee(new_button))
        new_button = QPushButton("In-Scene Choices")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+2

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.splf(new_button, 1))
        new_button = QPushButton("Conditional")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)+3

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)

        new_button.clicked.connect(lambda: self.con2(new_button))

        new_button = QPushButton("Variable")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 4

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.var(new_button))

    def var(self, button):
        index = self.groupBox.layout.indexOf(button)
        deln = index

        label = QtWidgets.QLabel('VARIABLE:')

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        label = QtWidgets.QLabel('Name of the variable:')
        index = index + 1
        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        label = QtWidgets.QLabel('Set, add, or subtract (write "-", "+", or "=").')

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        label = QtWidgets.QLabel('Write an integer or variable name.')

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        new_button = QPushButton("DELETE VARIABLE")

        # Find the index of the clicked button in the layout
        index = index + 1
        new_button.clicked.connect(lambda: self.DD2(new_button))
        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        '''self.groupBox.layout.removeWidget(button)
        button.deleteLater()'''
        for i in range(5):
            item = self.groupBox.layout.takeAt(deln - 4)
            if item.widget():
                item.widget().deleteLater()
        new_button.clicked.connect(lambda: self.add(new_button))
        self.groupBox.setLayout(self.groupBox.layout)
    def splf(self, button, num):

        label = QtWidgets.QLabel('IN-SCENE CHOICES:')
        self.num = num
        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)
        deln = index

        self.groupBox.layout.insertWidget(index + 1, label)

        self.addtbx(label,1)

        for i in range(5):
            item = self.groupBox.layout.takeAt(deln - 4)
            if item.widget():
                item.widget().deleteLater()
        '''label = QtWidgets.QLabel('Split ' + str(self.num))

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, label)
        label = QtWidgets.QLabel('Name of Split:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, label)
        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, tbx)

        new_button = QPushButton("Add to Split " + str(self.num))

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, new_button)
        new_button.clicked.connect(lambda: self.add(new_button))'''

        new_button = QPushButton("DELETE IN-SCENE CHOICES")

        # Find the index of the clicked button in the layout
        index = index + 3

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.dss(new_button, deln))

        label = QtWidgets.QLabel('END OF IN-SCENE CHOICES')
        self.num = num
        # Find the index of the clicked button in the layout
        index = index + 1
        deln = index

        self.groupBox.layout.insertWidget(index + 1, label)

        new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
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

        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        label = QtWidgets.QLabel('What is the dialogue?')

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = index + 1

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
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        '''self.groupBox.layout.removeWidget(button)
        button.deleteLater()'''
        for i in range(5):
            item = self.groupBox.layout.takeAt(deln - 4)
            if item.widget():
                item.widget().deleteLater()
        new_button.clicked.connect(lambda: self.add(new_button))
        self.groupBox.setLayout(self.groupBox.layout)

        '''index = self.groupBox.layout.indexOf(button)
        deln = index


        label = QtWidgets.QLabel('DIALOGUE:')

        index = self.groupBox.layout.indexOf(button)


        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index - 4, label)

        label = QtWidgets.QLabel('Name of the speaker:')
        index = self.groupBox.layout.indexOf(button)
        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index - 4, label)

        tbx =  QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index - 4, tbx)

        label = QtWidgets.QLabel('What is the dialogue?')

        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index - 4, label)
        tbx =  QtWidgets.QTextEdit(self)

        index = self.groupBox.layout.indexOf(button)
        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index - 4, tbx)
        new_button = QPushButton("DELETE DIALOGUE")

        index = self.groupBox.layout.indexOf(button)
        new_button.clicked.connect(lambda: self.DD(new_button))
        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index - 4, new_button)
        new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index - 3, new_button)
        new_button.clicked.connect(lambda: self.add(new_button))


        self.groupBox.layout.removeWidget(button)
        button.deleteLater()
        for i in range(5):
            item = self.groupBox.layout.takeAt(index-2)
            if item.widget():
                item.widget().deleteLater()
        self.groupBox.setLayout(self.groupBox.layout)'''

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
    def DD2(self, button):
        index = self.groupBox.layout.indexOf(button)
        for i in range(9):
            item = self.groupBox.layout.takeAt(index - 8)
            if item.widget():
                item.widget().deleteLater()

    def eee(self, button):
        label = QtWidgets.QLabel('END OF SCENE BRANCHES:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)
        deln = index

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)


        label = QtWidgets.QLabel('Type an existing scene or a new one:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 1


        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        self.addtbx2(label, 1)



        new_button = QPushButton("DELETE BRANCHES")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 5

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.delc(new_button,index))

        for i in range(5):
            item = self.groupBox.layout.takeAt(deln - 4)
            if item.widget():
                item.widget().deleteLater()
        # deleee = 0
        # lol = 0
        # for i in range(index-4,0,-1):
        #     widget = self.groupBox.layout.itemAt(i).widget()
        #     print(i)
        #     lol = lol + 1
        #     if isinstance(widget, QLabel):
        #         if widget.text() == "BRANCH:":
        #             deleee = i


        self.groupBox.setLayout(self.groupBox.layout)

    def delc(self, button, index):
        deleee = 0
        index = self.groupBox.layout.indexOf(button)
        lol = 0
        for i in range(index-1, 0, -1):
            widget = self.groupBox.layout.itemAt(i).widget()
            # print(i)
            lol = lol + 1
            if isinstance(widget, QLabel):
                if widget.text() == "END OF SCENE BRANCHES:":
                    deleee = i
                    break
        for i in range(lol+1):
            item = self.groupBox.layout.takeAt(deleee)
            if item.widget():
                item.widget().deleteLater()

    def addtbx2(self, button, n):
        index = self.groupBox.layout.indexOf(button)
        if (n > 1):
            item = self.groupBox.layout.takeAt(index)
            if item.widget():
                item.widget().deleteLater()



        label = QtWidgets.QLabel('Branch ' + str(n))

        # Find the index of the clicked button in the layout
        index = index - 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)
        n = n + 1
        new_button = QPushButton("Add another event")

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.addtbx2(new_button, n))

    def add2(self, button, num):

        #DO NOT DELETE THIS IS HOW TO READ TEXTEDIT
        #print(self.tbx.toPlainText())
        # DO NOT DELETE THIS IS HOW TO READ LINEEDIT
        # print(self.tbx.text())
        index = self.groupBox.layout.indexOf(button)



        # Create a new button
        new_button = QPushButton("Dialogue")

        # Find the index of the clicked button in the layout
        index = index - 2

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, new_button)
        new_button.clicked.connect(lambda: self.talking(new_button))
        new_button = QPushButton("End of Scene Branches")

        # Find the index of the clicked button in the layout
        index = index+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, new_button)
        new_button.clicked.connect(lambda: self.eee(new_button))
        new_button = QPushButton("In-Scene Choices")

        # Find the index of the clicked button in the layout
        index = index+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, new_button)
        new_button.clicked.connect(lambda: self.splf(new_button, 1))
        new_button = QPushButton("Conditional")

        # Find the index of the clicked button in the layout
        index = index+1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, new_button)

        new_button.clicked.connect(lambda: self.con2(new_button))

        new_button = QPushButton("Variable")

        # Find the index of the clicked button in the layout
        index = index +1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, new_button)
        new_button.clicked.connect(lambda: self.var(new_button))
        '''new_button = QPushButton("Add to Split " + str(num))

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.add2(new_button))

        new_button = QPushButton("DELETE SPLIT " + str(num))

        # Find the index of the clicked button in the layout
        index = index + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.ds(new_button, num))'''


    def con2(self, button):
        label = QtWidgets.QLabel('CONDITIONAL:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)
        deln = index
        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        label = QtWidgets.QLabel('IF:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)


        label = QtWidgets.QLabel('Variable Name:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 2

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 3

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        label = QtWidgets.QLabel('Condition (write "=", ">", "<", ">=", or "<="):')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 4

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 5

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        label = QtWidgets.QLabel('Write another variable name or an integer:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 6

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        tbx = QtWidgets.QTextEdit(self)

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 7

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, tbx)

        new_button1 = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 8

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button1)
        new_button1.clicked.connect(lambda: self.add(new_button1))

        label = QtWidgets.QLabel('END OF IF CONDITION')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 9

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        label = QtWidgets.QLabel('ELSE:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 10

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)



        new_button2 = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 11

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button2)
        new_button2.clicked.connect(lambda: self.add(new_button2))

        label = QtWidgets.QLabel('END OF ELSE CONDITION AND CONDITIONAL')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 12

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        new_button = QPushButton("DELETE CONDITIONAL")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 13

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.dcon(new_button, deln))

        new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 14

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.add(new_button))
        for i in range(5):
            item = self.groupBox.layout.takeAt(deln - 4)
            if item.widget():
                item.widget().deleteLater()

    def addtbx(self, button, num):


        label = QtWidgets.QLabel('Choice ' + str(num))

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button)

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)
        label = QtWidgets.QLabel('Name of Choice:')

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 1

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)


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
        new_button.clicked.connect(lambda: self.add2(new_button, num))

        new_button = QPushButton("DELETE CHOICE " + str(num))

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 4

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.ds(new_button, num))

        label = QtWidgets.QLabel('END OF CHOICE ' + str(num))

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 5

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, label)

        new_button = QPushButton("Add another choice")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 6

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index + 1, new_button)
        new_button.clicked.connect(lambda: self.addtbx(new_button, num + 1))

        '''new_button = QPushButton("Add")

        # Find the index of the clicked button in the layout
        index = self.groupBox.layout.indexOf(button) + 5

        # Insert the new button after the clicked button
        self.groupBox.layout.insertWidget(index, new_button)
        new_button.clicked.connect(lambda: self.add(new_button))'''
    def toggleUI(self):
        if (self.opened):
            self.close()
            self.opened = False
        else:
            self.show()
            self.opened = True

    def ds(self,button,n):
        deleee = 0
        index = self.groupBox.layout.indexOf(button)
        lol = 0
        for i in range(index - 1, 0, -1):
            widget = self.groupBox.layout.itemAt(i).widget()
            # print(i)
            lol = lol + 1
            if isinstance(widget, QLabel):
                if widget.text() == "Name of Choice:":
                    deleee = i
                    break
        for i in range(lol + 2):
            item = self.groupBox.layout.takeAt(deleee-1)
            if item.widget():
                item.widget().deleteLater()

    def dcon(self,button, index):
        deleee = 0
        index2 = self.groupBox.layout.indexOf(button)
        lol = 0
        for i in range(index-4, index2 + 1):
            item = self.groupBox.layout.takeAt(index-4)
            if item.widget():
                item.widget().deleteLater()


    def dss(self,button, index):
        deleee = 0
        index2 = self.groupBox.layout.indexOf(button)
        lol = 0
        for i in range(index - 4, index2 + 5):
            item = self.groupBox.layout.takeAt(index - 8)
            if item.widget():
                item.widget().deleteLater()

class HandHoldManager:
    def __init__(self):
        self.menu = None

    def menuToggle(self):
        if self.menu is None:
            self.menu = HandHoldMenu(self)
            self.menu.setWindowTitle("Hand Hold Menu")
            self.menu.setMinimumSize(QtCore.QSize(800, 600))

        # Toggle the visibility
        if self.menu.isVisible():
            self.menu.close()
        else:
            self.menu.show()
