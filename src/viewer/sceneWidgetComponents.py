import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMainWindow, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import *
        
class FocusableLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setFocusPolicy(Qt.StrongFocus)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.setStyleSheet("background-color: lightblue; padding: 5px;")

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.setStyleSheet("background-color: none; padding: 5px;")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab: 
            self.focusNextChild()
        else:
            super().keyPressEvent(event)

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

class _FocusableLabelDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 300, 500)
        mainWidget = QWidget(self)
        mainLayout = QVBoxLayout(mainWidget)

        for i in range(1, 8):
            label = FocusableLabel(f"Focusable Label {i}")
            mainLayout.addWidget(label)

        self.setCentralWidget(mainWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = _FocusableLabelDemo()
    window.show()
    sys.exit(app.exec_())
