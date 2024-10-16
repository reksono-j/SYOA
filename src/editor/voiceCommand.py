import speechToText
import keybinds
from util import randomFunctions
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent, QKeySequence
import sys


class VCManager():
    STT = None
    mainWindow = None
    shortcutsManager = None

    @staticmethod
    def getMainWindow():
        if VCManager.mainWindow is None:
            VCManager.mainWindow = VCManager.shortcutsManager.window
        
        return VCManager.mainWindow

    @staticmethod
    def getSTT():
        if VCManager.STT is None:
            VCManager.STT = speechToText.STT
        
        return VCManager.STT
    
    @staticmethod
    def getShortcutsManager():
        if VCManager.shortcutsManager is None:
            shortcutsManager = keybinds.ShortcutsManager.getInstance()
        
        return shortcutsManager

    @staticmethod
    def noShortcutFound(transcription:str, shortcutStr:str):
        print("shortcut does not exist: " + transcription)

    @staticmethod
    def VCCallback():
        if VCManager.getSTT().currentlyRecording:
            VCManager.getSTT().stopRecording()
        else:
            VCManager.getSTT().startRecording()

        if(not VCManager.getSTT().currentlyRecording):
                transcription = VCManager.getSTT().getLatestTranscription()
                shortcutStr = randomFunctions.stripShortcutsName(transcription)
                shortcutFunction = VCManager.getShortcutsManager().shortcutFunctionDict.get(shortcutStr)

                if(shortcutFunction is not None):
                    shortcutFunction() # calls the function associated with the shortcut
                else:
                    VCManager.noShortcutFound(transcription, shortcutStr)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("some window")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        self.button = QPushButton("some button", self)
        self.button.clicked.connect(self.buttonFunc)
        layout.addWidget(self.button)

        central_widget.setLayout(layout)
    
    def buttonFunc(self):
        self.textbox.setFocus()
        self.simulateKeyPress()
    
    def simulateKeyPress(self):
        someKeySequence = QKeySequence("aa")
        event = QKeyEvent(QEvent.KeyPress,someKeySequence[0],Qt.NoModifier)
        QApplication.sendEvent(self.textbox, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec())


