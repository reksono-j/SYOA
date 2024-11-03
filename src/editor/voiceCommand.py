import speechToText
import keybinds
from util import randomFunctions
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit, QGridLayout,
)
from PySide6.QtCore import Qt
import sys


class VCManager():
    STT = None
    mainWindow = None
    shortcutsManager = None
    overlay = None
    overlayText = None
    recordAgainButton = None
    quitButton = None

    @staticmethod
    def getMainWindow():
        if VCManager.mainWindow is None:
            VCManager.mainWindow = VCManager.getShortcutsManager().window
        
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
    def initializeWidgets():
        # parent overlay widget
        VCManager.overlay = QWidget()
        VCManager.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.75);")
        
        # button1
        VCManager.recordAgainButton = QPushButton("Record")
        VCManager.recordAgainButton.setParent(VCManager.overlay)
        VCManager.recordAgainButton.clicked.connect(VCManager.recordAgainFunction)

        # button2
        VCManager.quitButton = QPushButton("Quit")
        VCManager.quitButton.setParent(VCManager.overlay)
        VCManager.quitButton.clicked.connect(VCManager.quitButtonFunction)

        # text
        VCManager.overlayText = QLabel("")
        VCManager.overlayText.setParent(VCManager.overlay)
        VCManager.overlayText.setStyleSheet("color: white; font-size: 30px;")

        # layout
        layout = QGridLayout()
        layout.addWidget(VCManager.overlayText,0,0,1,2,Qt.AlignCenter)
        layout.addWidget(VCManager.recordAgainButton,1,0)
        layout.addWidget(VCManager.quitButton,1,1)

        VCManager.overlay.setLayout(layout)
        VCManager.overlay.hide()

    @staticmethod
    def getOverlay():
        if VCManager.overlay is None:
            VCManager.initializeWidgets()
            
        return VCManager.overlay

    @staticmethod
    def getOverlayText():
        if VCManager.overlayText is None:
            VCManager.initializeWidgets()
        
        return VCManager.overlayText

    @staticmethod
    def getRecordAgainButton():
        if VCManager.recordAgainButton is None:
            VCManager.initializeWidgets()
            

        return VCManager.recordAgainButton
    
    @staticmethod
    def recordAgainFunction():
        VCManager.hideOverlay()
        VCManager.VCCallback()

    @staticmethod
    def getQuitButton():
        if VCManager.quitButton is None:
           VCManager.initializeWidgets()

        return VCManager.quitButton
    
    @staticmethod
    def quitButtonFunction():
        VCManager.hideOverlay()

    @staticmethod
    def showOverlay():
        MainWindow =  VCManager.getMainWindow()
        VCManager.getOverlay().setParent(MainWindow)
        VCManager.getOverlay().setGeometry(MainWindow.rect())
        VCManager.getOverlay().show()

    @staticmethod
    def hideOverlay():
        VCManager.getOverlay().hide()

    @staticmethod
    def setOverlayText(s):
        VCManager.getOverlayText().setText(s)

    @staticmethod
    def noShortcutFound(transcription:str, shortcutStr:str):
        print("Shortcut does not exist: " + transcription)
        VCManager.setOverlayText("Shortcut does not exist: " + transcription)
        VCManager.showOverlay()

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
                    VCManager.hideOverlay()
                else:
                    VCManager.noShortcutFound(transcription, shortcutStr)


if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("some window")
            self.setGeometry(100, 100, 1200, 800)

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
            VCManager.noShortcutFound("some random transcriptions","")

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    VCManager.mainWindow = w

    sys.exit(app.exec())


