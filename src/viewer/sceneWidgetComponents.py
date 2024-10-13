import sys
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import *
        

class NonActivatableButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True
        self.setStyleSheet("text-align: left; padding: 5px;")
    
    def setActive(self, active):
        self.active = active
        if active:
            self.setStyleSheet("text-align: left; padding: 5px;")
        else:
            self.setStyleSheet("background-color: lightgray; color: black; border: 1px solid darkgray; text-align: left; padding: 5px;")

    def mousePressEvent(self, event):
        if self.active:
            super().mousePressEvent(event)
        else:
            event.ignore()
            
    def keyPressEvent(self, event):
        if self.active:
            super().keyPressEvent(event)
        else:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                event.ignore()