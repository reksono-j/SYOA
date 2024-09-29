import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class HandHoldMenu(QWidget):
    def __init__(self, UICustomizeManager, parent):
        super(HandHoldMenu, self).__init__(parent)
        self.parent = parent
        self.HandHoldManager = HandHoldManager
        self.initParameters()
        self.initUI()
      
    def initParameters(self):
        self.opened = False  
   
    def initUI(self):
        # printing pressed
        print("pressed")
        count = 0
        title = True

        self.layout = QVBoxLayout()
        self.label = QLabel('Give a title for this event:', self)
        self.label.setGeometry(count,100,200,30)
        self.layout.addWidget(self.label)
        self.tbx = QTextEdit(self)
        count = count + 30
        self.tbx.setGeometry(100, count, 100, 30)
        self.layout.addWidget(self.tbx)
        self.button = QPushButton("Enter", self)
        self.button.setGeometry(200, count, 100, 30)
        self.layout.addWidget(self.button)
        count = count + 30
        self.label = QLabel('Do you want to add dialogue?', self)
        self.label.setGeometry(100, count, 300, 30)
        self.layout.addWidget(self.label)
        self.tbx = QTextEdit(self)
        count = count + 30
        self.tbx.setGeometry(100, count, 100, 30)
        self.layout.addWidget(self.tbx)

        self.button = QPushButton("Enter", self)
        self.button.setGeometry(200, count, 100, 30)
        self.layout.addWidget(self.button)
        count = count + 30
        self.label = QLabel('Who is talking?', self)
        self.label.setGeometry(100, count, 300, 30)
        self.layout.addWidget(self.label)
        self.tbx = QTextEdit(self)
        count = count + 30
        self.tbx.setGeometry(100, count, 100, 30)
        self.layout.addWidget(self.tbx)

        self.button = QPushButton("Enter", self)
        self.button.setGeometry(200, count, 100, 30)
        self.layout.addWidget(self.button)
        count = count + 30
        self.label = QLabel('What is the dialogue?', self)
        self.label.setGeometry(100, count, 300, 30)
        self.layout.addWidget(self.label)
        self.tbx = QTextEdit(self)
        count = count + 30
        self.tbx.setGeometry(100, count, 100, 30)
        self.layout.addWidget(self.tbx)

        self.button = QPushButton("Enter", self)
        self.button.setGeometry(200, count, 100, 30)
        self.layout.addWidget(self.button)
        count = count + 30
        self.label = QLabel('Do you want this to connect to a existing or new event? Is this the end of the story?', self)
        self.label.setGeometry(100, count, 600, 30)
        self.layout.addWidget(self.label)
        self.tbx = QTextEdit(self)
        count = count + 30
        self.tbx.setGeometry(100, count, 100, 30)
        self.layout.addWidget(self.tbx)
        self.button = QPushButton("Enter", self)
        self.button.setGeometry(200, count, 100, 30)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.close()

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
