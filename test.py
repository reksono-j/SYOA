
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
    def getOverlay():
        if VCManager.overlay is None:
            # overlay things
            VCManager.overlay = QWidget()
            VCManager.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
            layout = QGridLayout()
            VCManager.overlay.setLayout(layout)
            VCManager.overlay.hide()

            # just to initialize everything
            VCManager.getOverlayText()
            VCManager.getQuitButton()
            VCManager.getRecordAgainButton()
            
        return VCManager.overlay

    @staticmethod
    def getOverlayText():
        if VCManager.overlayText is None:
            VCManager.overlayText = QLabel("Some text idk", VCManager.getOverlay())
            VCManager.overlayText.setStyleSheet("color: white; font-size: 30px;")
            VCManager.getOverlay().layout().addWidget(VCManager.overlayText,0,0,1,2,Qt.AlignCenter)
        
        return VCManager.overlayText

    @staticmethod
    def getRecordAgainButton():
        if VCManager.recordAgainButton is None:
            button = QPushButton("Record", VCManager.getOverlay())
            VCManager.getOverlay().layout().addWidget(button,1,0)


        return VCManager.recordAgainButton
    
    @staticmethod
    def getQuitButton():
        if VCManager.quitButton is None:
            button = QPushButton("Quit", VCManager.getOverlay())
            VCManager.getOverlay().layout().addWidget(button,1,1)

        return VCManager.quitButton
    
    @staticmethod
    def showOverlay():
        MainWindow =  VCManager.getMainWindow()
        print(type(MainWindow))
        VCManager.getOverlay().setParent(MainWindow)
        VCManager.getOverlay().setGeometry(MainWindow.rect())
        VCManager.getOverlayText().setGeometry(MainWindow.rect())
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
        #VCManager.setOverlayText("Shortcut does not exist: " + transcription)
        VCManager.showOverlay()
        # not done yet

    @staticmethod
    def VCCallback():
        VCManager.showOverlay()
        #if VCManager.getSTT().currentlyRecording:
        #    VCManager.getSTT().stopRecording()
        #else:
        #    VCManager.getSTT().startRecording()
#
        #if(not VCManager.getSTT().currentlyRecording):
        #        transcription = VCManager.getSTT().getLatestTranscription()
        #        shortcutStr = randomFunctions.stripShortcutsName(transcription)
        #        shortcutFunction = VCManager.getShortcutsManager().shortcutFunctionDict.get(shortcutStr)
#
        #        if(shortcutFunction is not None):
        #            shortcutFunction() # calls the function associated with the shortcut
        #        else:
        #            VCManager.noShortcutFound(transcription, shortcutStr)


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
        VCManager.showOverlay()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    VCManager.mainWindow = w

    sys.exit(app.exec())


