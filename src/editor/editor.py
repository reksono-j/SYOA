import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import keybinds

import ui_customize
import handhold
import ide


class Window(QMainWindow):
   def __init__(self):
      super().__init__()

      # setting title
      self.setWindowTitle("Editor")

      # setting default geometry
      self.window_xPos = 100
      self.window_yPos = 100
      self.window_width = 1200
      self.window_height = 800
      self.setGeometry(self.window_xPos, self.window_yPos, self.window_width, self.window_height)
      self.setFixedSize(1200, 800)

      # calls error if no central widget (essentially main window)
      self.centralWidget = QWidget(self)
      self.setCentralWidget(self.centralWidget)
      self.centralWidget.layout = QVBoxLayout()
      self.centralWidget.layout.setSpacing(0)
      self.centralWidget.layout.setContentsMargins(0, 0, 0, 0)
      # self.centralWidget.sizePolicy = QSizePolicy()
      # self.centralWidget.sizePolicy.setVerticalPolicy(QSizePolicy.Fixed)
      # self.centralWidget.sizePolicy.setHorizontalPolicy(QSizePolicy.Fixed)

      # widget that holds buttons that switch to different menus
      self.buttonsWidget = QWidget(self.centralWidget)
      self.buttonsWidget.layout = QHBoxLayout()
      self.buttonsWidget.layout.setSpacing(10)
      # self.buttonsWidget.sizePolicy = QSizePolicy()
      # self.buttonsWidget.sizePolicy.setVerticalPolicy(QSizePolicy.Fixed)
      # self.buttonsWidget.sizePolicy.setHorizontalPolicy(QSizePolicy.Fixed)

      self.centralWidget.layout.addWidget(self.buttonsWidget)

      # stacked widget that holds and shows/closes different menus
      self.menusWidget = QStackedWidget(self.centralWidget)

      #adding menus and buttons widgets to central widget
      self.centralWidget.layout.addWidget(self.menusWidget)
      self.centralWidget.layout.addWidget(self.buttonsWidget)

      # ui customize menu import
      self.uiSettingsManager = ui_customize.UICustomizeManager(self)
      self.uiSettingsManager.applySettings()

      # hand hold menu import
      self.handholdManager = handhold.HandHoldManager(self)

      # ide menu import
      self.ideManager = ide.IDEManager(self)

      # calling method
      self.UiComponents()

      # showing all the widgets
      self.show()

      # keybinds stuff
      shortcutsManager = keybinds.ShortcutsManager(self)

      # setting previously defined layouts of central and buttons widget
      self.centralWidget.setLayout(self.centralWidget.layout)
      self.buttonsWidget.setLayout(self.buttonsWidget.layout)


   # method for widgets
   def UiComponents(self):
      # add widgets associated with each push button to central stacked widget
      self.menusWidget.addWidget(self.handholdManager.menu)
      self.menusWidget.addWidget(self.ideManager.menu)
      self.menusWidget.addWidget(self.uiSettingsManager.menu)

      # creating a push button
      self.button = QPushButton("IDE")

      # adding action to a button
      self.button.clicked.connect(lambda: self.menusWidget.setCurrentWidget(self.ideManager.menu))

      # creating a push button
      self.button1 = QPushButton("Hand Hold")

      # adding action to a button
      self.button1.clicked.connect(lambda: self.menusWidget.setCurrentWidget(self.handholdManager.menu))

      # ui settings button setup
      self.buttonUISettings = QPushButton("UI Settings")
      self.buttonUISettings.clicked.connect(lambda: self.menusWidget.setCurrentWidget(self.uiSettingsManager.menu))

      # adding defined buttons to buttons widget
      self.buttonsWidget.layout.addWidget(self.button)
      self.buttonsWidget.layout.addWidget(self.button1)
      self.buttonsWidget.layout.addWidget(self.buttonUISettings)



# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
