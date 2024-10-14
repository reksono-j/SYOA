import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class IDEMenu(QTextEdit):
    def __init__(self, UICustomizeManager, parent):
        super(IDEMenu, self).__init__(parent)
        self.parent = parent
        self.IDEManager = IDEManager
        self.initParameters()
        self.initUI()
      
    def initParameters(self):
        self.opened = False  
   
    def initUI(self):
      self.close()

    def toggleUI(self):
        if (self.opened):
            self.close()
            self.opened = False
        else:
            self.show()
            self.opened = True

class IDEManager:
    def __init__(self, window) -> None:
        self.window = window
        self.menu = IDEMenu(self, window)

    def menuToggle(self):
        self.menu.toggleUI()
