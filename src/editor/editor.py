import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import keybinds


class Window(QMainWindow):
   def __init__(self):
      super().__init__()

      # setting title
      self.setWindowTitle("Editor")

      # setting geometry
      self.setGeometry(100, 100, 1200, 800)

      # calling method
      self.UiComponents()

      # showing all the widgets
      self.show()

      # keybinds stuff
      shortcutsManager = keybinds.ShortcutsManager(self)
      


   # method for widgets
   def UiComponents(self):
      # creating a push button
      self.button = QPushButton("IDE", self)

      # setting geometry of button
      self.button.setGeometry(1100, 0, 100, 30)

      # adding action to a button
      self.button.clicked.connect(self.IDE)
      self.button1 = QPushButton("Hand Hold", self)

      # setting geometry of button
      self.button1.setGeometry(0, 0, 100, 30)

      # adding action to a button
      self.button1.clicked.connect(self.clickme)



   # action method
   def clickme(self):
      # printing pressed
      print("pressed")
      count = 100
      title = True

      self.label = QLabel('Give a title for this event:', self)
      self.label.setGeometry(count,100,200,30)
      self.layout().addWidget(self.label)
      self.tbx = QTextEdit(self)
      count = count + 30
      self.tbx.setGeometry(100, count, 100, 30)
      self.layout().addWidget(self.tbx)
      self.button = QPushButton("Enter", self)
      self.button.setGeometry(200, count, 100, 30)
      self.layout().addWidget(self.button)
      count = count + 30
      self.label = QLabel('Do you want to add dialogue?', self)
      self.label.setGeometry(100, count, 300, 30)
      self.layout().addWidget(self.label)
      self.tbx = QTextEdit(self)
      count = count + 30
      self.tbx.setGeometry(100, count, 100, 30)
      self.layout().addWidget(self.tbx)

      self.button = QPushButton("Enter", self)
      self.button.setGeometry(200, count, 100, 30)
      self.layout().addWidget(self.button)
      count = count + 30
      self.label = QLabel('Who is talking?', self)
      self.label.setGeometry(100, count, 300, 30)
      self.layout().addWidget(self.label)
      self.tbx = QTextEdit(self)
      count = count + 30
      self.tbx.setGeometry(100, count, 100, 30)
      self.layout().addWidget(self.tbx)

      self.button = QPushButton("Enter", self)
      self.button.setGeometry(200, count, 100, 30)
      self.layout().addWidget(self.button)
      count = count + 30
      self.label = QLabel('What is the dialogue?', self)
      self.label.setGeometry(100, count, 300, 30)
      self.layout().addWidget(self.label)
      self.tbx = QTextEdit(self)
      count = count + 30
      self.tbx.setGeometry(100, count, 100, 30)
      self.layout().addWidget(self.tbx)

      self.button = QPushButton("Enter", self)
      self.button.setGeometry(200, count, 100, 30)
      self.layout().addWidget(self.button)
      count = count + 30
      self.label = QLabel('Do you want this to connect to a existing or new event? Is this the end of the story?', self)
      self.label.setGeometry(100, count, 600, 30)
      self.layout().addWidget(self.label)
      self.tbx = QTextEdit(self)
      count = count + 30
      self.tbx.setGeometry(100, count, 100, 30)
      self.layout().addWidget(self.tbx)
      self.button = QPushButton("Enter", self)
      self.button.setGeometry(200, count, 100, 30)
      self.layout().addWidget(self.button)

   def IDE(self):

      print("Meow")
      self.tbx = QTextEdit(self)
      print("Meow")
      self.tbx.setGeometry(0, 100, 1200, 700)
      self.layout().addWidget(self.tbx)






# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
