import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Window(QMainWindow):
   def __init__(self):
      super().__init__()

      # setting title
      self.setWindowTitle("Player")

      # setting geometry
      self.setGeometry(100, 100, 1200, 800)

      # calling method
      self.UiComponents()

      # showing all the widgets
      self.show()

   # method for widgets
   def UiComponents(self):


       self.label = QLabel('The Beginning', self)
       self.label.setGeometry(100, 100, 200, 30)
       self.layout().addWidget(self.label)

       self.label = QLabel('Bob: "How is your day going?"', self)
       self.label.setGeometry(100, 130, 200, 30)
       self.layout().addWidget(self.label)

       self.label = QLabel('Jim: "Well. Do you want to play video games or go to the gym today?', self)
       self.label.setGeometry(100, 160, 2000, 30)
       self.layout().addWidget(self.label)

       self.label = QLabel('Select 1 for "Play Video Games". Select 2 for "Go to the Gym".', self)
       self.label.setGeometry(100, 190, 2000, 30)
       self.layout().addWidget(self.label)

       self.button = QPushButton("1", self)
       self.button.setGeometry(100, 220, 100, 30)
       self.layout().addWidget(self.button)
       self.button.clicked.connect(self.clickme)


       self.button = QPushButton("2", self)
       self.button.setGeometry(200, 220, 100, 30)
       self.layout().addWidget(self.button)

       self.button.clicked.connect(self.IDE)


   # action method
   def clickme(self):
       self.label = QLabel('Play Video Games', self)
       self.label.setGeometry(100, 250, 200, 30)
       self.layout().addWidget(self.label)

       self.label = QLabel('Bob: "I want to play video games today. What video games do you have?"', self)
       self.label.setGeometry(100, 280, 2000, 30)
       self.layout().addWidget(self.label)

       self.label = QLabel('Jim: "I have Madden or Call of Duty."', self)
       self.label.setGeometry(100, 310, 2000, 30)
       self.layout().addWidget(self.label)

       self.label = QLabel('Select 1 for "Play Madden". Select 2 for "Play Call of Duty".', self)
       self.label.setGeometry(100, 340, 2000, 30)
       self.layout().addWidget(self.label)

       self.button = QPushButton("1", self)
       self.button.setGeometry(100, 370, 100, 30)
       self.layout().addWidget(self.button)

       self.button = QPushButton("2", self)
       self.button.setGeometry(200, 370, 100, 30)
       self.layout().addWidget(self.button)

   def IDE(self):
       self.label = QLabel('Go to the Gym', self)
       self.label.setGeometry(100, 250, 200, 30)
       self.layout().addWidget(self.label)

       self.label = QLabel('Bob: "Let\'s go to the gym."', self)
       self.label.setGeometry(100, 280, 200, 30)
       self.layout().addWidget(self.label)

       self.label = QLabel('Jim: "We can do chest and arms or legs."', self)
       self.label.setGeometry(100, 310, 2000, 30)
       self.layout().addWidget(self.label)

       self.label = QLabel('Select 1 for "Chest and Arm Workout". Select 2 for "Leg Workout".', self)
       self.label.setGeometry(100, 340, 2000, 30)
       self.layout().addWidget(self.label)

       self.button = QPushButton("1", self)
       self.button.setGeometry(100, 370, 100, 30)
       self.layout().addWidget(self.button)

       self.button = QPushButton("2", self)
       self.button.setGeometry(200, 370, 100, 30)
       self.layout().addWidget(self.button)






# create PySide6 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
