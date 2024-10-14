import sys
from PySide6 import QtWidgets

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
        count = 100
        title = True

        self.label = QtWidgets.QLabel('Give a title for this event:', self)
        self.label.setGeometry(count,100,200,30)
        self.groupBox.layout.addWidget(self.label)
        self.tbx = QtWidgets.QTextEdit(self)
        self.tbx.setAccessibleName("Event title text box. ")
        self.tbx.setAccessibleDescription("Insert an event title here.")
        self.count = count + 30
        count = self.count
        self.tbx.setGeometry(100, count, 100, 30)
        self.groupBox.layout.addWidget(self.tbx)
        button = QtWidgets.QPushButton("Enter", self)
        button.setGeometry(200, count, 100, 30)
        self.groupBox.layout.addWidget(button)
        self.count = count + 30
        button.clicked.connect(self.test)
        if button.clicked:
            print("hello")
        self.groupBox.setLayout(self.groupBox.layout)



    def test(self):

        count = self.count
        self.label = QtWidgets.QLabel('Do you want to add dialogue?', self)
        self.label.setAccessibleName("Do you want to add dialogue?")
        self.label.setAccessibleDescription("Answer with following buttons")
        self.label.setGeometry(100, count, 300, 30)
        self.groupBox.layout.addWidget(self.label)
        count = count + 30
        self.button = QtWidgets.QPushButton("Yes", self)
        self.button.setGeometry(100, count, 100, 30)
        self.groupBox.layout.addWidget(self.button)
        count = count + 30
        self.count = count
        self.button.clicked.connect(self.talking)
        self.button = QtWidgets.QPushButton("No", self)
        self.button.setGeometry(200, count-30, 100, 30)
        self.groupBox.layout.addWidget(self.button)
        self.button.clicked.connect(self.eee)
        self.groupBox.setLayout(self.groupBox.layout)

    def talking(self):
        count = self.count
        self.label = QtWidgets.QLabel('Who is talking?', self)
        self.label.setGeometry(100, count, 300, 30)
        self.groupBox.layout.addWidget(self.label)
        self.tbx = QtWidgets.QTextEdit(self)
        self.tbx.setAccessibleName("Speaker name text box.")
        self.tbx.setAccessibleDescription("Insert the speaker name.")
        count = count + 30
        self.tbx.setGeometry(100, count, 100, 30)
        self.groupBox.layout.addWidget(self.tbx)

        self.button = QtWidgets.QPushButton("Enter", self)
        self.button.setGeometry(200, count, 100, 30)
        self.groupBox.layout.addWidget(self.button)
        count = count + 30
        self.count = count
        self.button.clicked.connect(self.WD)
        self.groupBox.setLayout(self.groupBox.layout)

    def WD(self):
        count = self.count
        self.label = QtWidgets.QLabel('What is the dialogue?', self)
        self.label.setGeometry(100, count, 300, 30)
        self.groupBox.layout.addWidget(self.label)
        self.tbx = QtWidgets.QTextEdit(self)
        self.tbx.setAccessibleName("Speaker dialogue text box.")
        self.tbx.setAccessibleDescription("Insert the dialogue for the speaker.")
        count = count + 30
        self.tbx.setGeometry(100, count, 100, 30)
        self.groupBox.layout.addWidget(self.tbx)

        self.button = QtWidgets.QPushButton("Enter", self)
        self.button.setGeometry(200, count, 100, 30)
        self.groupBox.layout.addWidget(self.button)
        count = count + 30
        self.count = count
        self.button.clicked.connect(self.test)
        self.groupBox.setLayout(self.groupBox.layout)

    def eee(self):
        count = self.count
        self.label = QtWidgets.QLabel('Do you want this to connect to a existing or new event? Is this the end of the story?', self)
        self.label.setAccessibleName('Do you want this to connect to a existing or new event? Is this the end of the story?')
        self.label.setAccessibleDescription("Answer with following buttons")
        self.label.setGeometry(100, count, 600, 30)
        self.groupBox.layout.addWidget(self.label)
        self.tbx = QtWidgets.QTextEdit(self)
        count = count + 30
        self.button = QtWidgets.QPushButton("Existing", self)
        self.button.setGeometry(100, count, 100, 30)
        self.groupBox.layout.addWidget(self.button)
        count = count + 30
        self.count = count
        self.button.clicked.connect(self.talking)
        self.button = QtWidgets.QPushButton("New", self)
        self.button.setGeometry(200, count - 30, 100, 30)
        self.groupBox.layout.addWidget(self.button)
        self.button = QtWidgets.QPushButton("End", self)
        self.button.setGeometry(300, count - 30, 100, 30)
        self.groupBox.layout.addWidget(self.button)

        self.groupBox.setLayout(self.groupBox.layout)

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
