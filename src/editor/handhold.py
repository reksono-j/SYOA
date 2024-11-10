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
        self.count = 100
        title = True

        self.label = QtWidgets.QLabel('Give a title for this event:', self)
        self.label.setGeometry(self.count,100,200,30)
        self.groupBox.layout.addWidget(self.label)
        self.tbx = QtWidgets.QTextEdit(self)
        self.tbx.setAccessibleName("Event title text box. ")
        self.tbx.setAccessibleDescription("Insert an event title here.")
        self.count = self.count + 30
        count = self.count
        self.tbx.setGeometry(100, self.count, 100, 30)
        self.groupBox.layout.addWidget(self.tbx)
        button = QtWidgets.QPushButton("Add", self)
        button.setGeometry(200, self.count, 100, 30)
        self.groupBox.layout.addWidget(button)
        self.count = button.y()
        print(self.count)
        button.clicked.connect(self.add)
        if button.clicked:
            print("hello")
        self.groupBox.setLayout(self.groupBox.layout)


    def add(self):
        button = QtWidgets.QPushButton("Dialogue", self)
        button.setGeometry(200, self.count, 100, 30)
        self.groupBox.layout.addWidget(button)
        self.count = button.y()
        print(self.count)
        button.clicked.connect(self.talking)
        if button.clicked:
            print("hello")
        button = QtWidgets.QPushButton("Choice", self)
        button.setGeometry(200, self.count, 100, 30)
        self.groupBox.layout.addWidget(button)
        self.count = button.y()
        button.clicked.connect(self.add)
        if button.clicked:
            print("hello")
        button = QtWidgets.QPushButton("Split", self)
        button.setGeometry(200, self.count, 100, 30)
        self.groupBox.layout.addWidget(button)
        self.count = button.y()
        button.clicked.connect(self.eee)
        if button.clicked:
            print("hello")
        button = QtWidgets.QPushButton("Option 4", self)
        button.setGeometry(200, self.count, 100, 30)
        self.groupBox.layout.addWidget(button)

        self.count = button.y()
        button.clicked.connect(self.add)
        if button.clicked:
            print("hello")


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
        self.button = QtWidgets.QPushButton("Add", self)
        self.button.setGeometry(200, count, 100, 30)
        self.groupBox.layout.addWidget(self.button)
        self.count = self.button.y()
        print(self.count)
        self.button.clicked.connect(self.add)
        self.groupBox.setLayout(self.groupBox.layout)



    def eee(self):
        count = self.count
        self.label = QtWidgets.QLabel('Choose an existing event or type a new one.', self)
        self.label.setAccessibleName('Choose an existing event or type a new one.')
        self.label.setAccessibleDescription("Answer with following buttons")
        self.label.setGeometry(100, self.count, 600, 30)
        self.groupBox.layout.addWidget(self.label)
        self.tbx = QtWidgets.QTextEdit(self)
        count = count + 30
        self.button = QtWidgets.QPushButton("Existing", self)
        self.button.setGeometry(100, self.count, 100, 30)
        self.groupBox.layout.addWidget(self.button)
        count = count + 30
        self.tbx = QtWidgets.QTextEdit(self)
        self.tbx.setAccessibleName("Speaker dialogue text box.")
        self.tbx.setAccessibleDescription("Insert the dialogue for the speaker.")
        button = QtWidgets.QPushButton("Add", self)
        count = count + 30
        self.tbx.setGeometry(100, self.count, 100, 30)
        self.groupBox.layout.addWidget(self.tbx)
        button.setGeometry(200, self.count, 100, 30)
        self.groupBox.layout.addWidget(button)
        self.count = button.y()
        button.clicked.connect(self.add)
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
