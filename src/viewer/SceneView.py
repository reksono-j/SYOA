import sys, os
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QTextEdit, QMainWindow, QPushButton, 
    QWidget, QVBoxLayout, QDialog, QStackedWidget, QLabel,
    QScrollArea
)
from PySide6.QtCore import QRect, QPropertyAnimation, QEasingCurve, Qt, QTimer, Signal, QCoreApplication
from PySide6.QtGui import QFont, QPalette, QColor, QPainter, QPixmap
from src.viewer.loader import Loader
from src.viewer.audioManager import AudioManager
from src.viewer.variables import ViewerVariableManager
from src.viewer.backgroundManager import BackgroundManager
from src.viewer.files import FileManager, SaveManagerGUI, SaveManager
from options import UICustomizeDialog

class DialogueLog(QWidget):
    def __init__(self, getHistoryCallback):
        super().__init__()
        self.getHistoryCallback = getHistoryCallback
        self.initUI()
        self.setStyleSheet("""
            QWidget#dialogueLog {
                border-radius: 10px;
                background-color: #333;
                border: 1px solid #3498db;
            }
            QWidget::hover#dialogueLog {
                border: 5px solid #3498db;
            }
            #dialogueLog QTextEdit {
                border: none;
                border-radius: 5px;
                background-color: #3498db;
                color: white;
            }
            #dialogueLog QTextEdit::Focus {
                background-color: #009999;
            }
        """)

    def initUI(self):
        self.scrollArea = QScrollArea(self)
        self.scrollAreaWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollAreaWidget)
        self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.scrollLayout.setSpacing(15)
        self.scrollAreaWidget.setLayout(self.scrollLayout)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.scrollToBottom)
        
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.scrollArea.setWidgetResizable(True)
        self.setCentralWidget(self.scrollArea)

        log = self.getHistoryCallback()
        for i in range(log):
            textToDisplay = ""
            if (i % 2 == 0):
              textToDisplay = f"This is dynamic text {i + 1}. This is a test to see if the dynamic resizing works. I'm going to give this some extra text."
            else:
              textToDisplay = f"This is dynamic text {i + 1}. ."
            self.createContainer(textToDisplay, self.scrollLayout)

        # Scroll to the bottom initially
        self.scrollToBottom()

    def createContainer(self, textToDisplay, scrollLayout):
        container = QWidget(self)
        container.setObjectName("dialogueLog")
        layout = QVBoxLayout(container)

        textBox = QTextEdit(container)
        textBox.setReadOnly(True)
        textBox.setStyleSheet("padding:10px;")
        font = QFont("Arial", 24, QFont.Weight.Bold)
        textBox.setCurrentFont(font)
        textBox.document().setDefaultFont(font)
        textBox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        textBox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        textBox.setText(textToDisplay)

        layout.addWidget(textBox)

        scrollLayout.addWidget(container)
        self.adjustSizeToContent(container, textBox, textToDisplay)

    def adjustSizeToContent(self, container, textBox, textToDisplay):
        document = textBox.document().clone()
        document.setPlainText(textToDisplay)

        maxWidth = self.width() * 0.75
        document.setTextWidth(maxWidth)
        contentSize = document.size()
        frameWidth = textBox.frameWidth()
        extraHeightPadding = 0
        totalPadding = frameWidth * 2 + extraHeightPadding

        newWidth = contentSize.width() + totalPadding
        newHeight = contentSize.height() + totalPadding

        textBox.setFixedSize(newWidth, newHeight)
        container.setFixedSize(newWidth + 20, newHeight + 20)

    def scrollToBottom(self):
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
        
class SceneViewMenuOverlay(QWidget):
    closeMenu = Signal()
    
    BUTTON_STYLE = """
        QPushButton {
            background-color: #3498db;
            color: white;
            padding: 20px 40px; 
            border-radius: 12px; 
            font-size: 20px; 
            font-weight: bold;
            min-width: 70px;
            min-height: 30px; 
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #2471a3;
        }
    """
    def __init__(self, getSaveDataCallback, loadSaveFileCallback, parent=None):
        super().__init__(parent)
        
        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.setWindowFlags(Qt.FramelessWindowHint) 
        
        self.layout = QVBoxLayout(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)  

        self.menuStack = QStackedWidget()
        self.menuStack.setStyleSheet("background: transparent; border: none;")
        self.layout.addWidget(self.menuStack)

        self.pauseMenu = self.createPauseMenu()
        self.saveMenu = SaveManagerGUI(True, getSaveDataCallback, self.parent().toggleMenuOverlay, self)
        self.loadMenu = SaveManagerGUI(False, loadSaveFileCallback, self.parent().toggleMenuOverlay, self)
        self.settingsMenu = self.createSettingsMenu()

        self.menuStack.addWidget(self.pauseMenu)
        self.menuStack.addWidget(self.saveMenu)
        self.menuStack.addWidget(self.loadMenu)
        #self.menuStack.addWidget(self.settingsMenu)

        self.menuStack.setCurrentWidget(self.pauseMenu)
    
    def emitLoadSignal(self, filepath: str):
        self.loadFile.emit(filepath)
    
    
    def createPauseMenu(self):
        menu = QWidget()
        layout = QVBoxLayout(menu)
        layout.setAlignment(Qt.AlignCenter)

        layout.setSpacing(20) 
        
        resumeButton = QPushButton("Resume")
        saveButton = QPushButton("Save")
        loadButton = QPushButton("Load")
        settingsButton = QPushButton("Settings")
        quitButton = QPushButton("Quit")

        for btn in [resumeButton, saveButton, loadButton, settingsButton, quitButton]:
            btn.setStyleSheet(self.BUTTON_STYLE)
            layout.addWidget(btn)

        resumeButton.clicked.connect(self.closeMenu.emit) 
        saveButton.clicked.connect(lambda: self.menuStack.setCurrentWidget(self.saveMenu))
        loadButton.clicked.connect(lambda: self.menuStack.setCurrentWidget(self.loadMenu))
        settingsButton.clicked.connect(lambda: self.settingsMenu.exec())
        quitButton.clicked.connect(QCoreApplication.quit)

        return menu

    def createSettingsMenu(self):
        # menu = QWidget()
        # layout = QVBoxLayout(menu)
        # layout.setAlignment(Qt.AlignCenter)

        # warningLabel = QLabel("OUT OF ORDER")
        # warningLabel.setStyleSheet("font-size: 32px; color: white;")
        # layout.addWidget(warningLabel)

        # backButton = QPushButton("Back")
        # backButton.setStyleSheet(self.BUTTON_STYLE)
        # backButton.clicked.connect(lambda: self.menuStack.setCurrentWidget(self.pauseMenu))
        # layout.addWidget(backButton)

        # return menu
        return UICustomizeDialog()

    def switchToPauseMenu(self):
        self.menuStack.setCurrentWidget(self.pauseMenu)
        
class SceneView(QMainWindow):
    def __init__(self, filePath, freshStart):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(1280, 720)
                
        self.audio = AudioManager()
        
        self.backgroundManager = BackgroundManager()
        self.background = self.backgroundManager.getBackground()
        self.setCentralWidget(self.background)
        self.background.setGeometry(self.rect())
        self.backgroundPath = ""
        
        self.dialogueHistory = []
        self.nextEntry = {}
        self.currentBGM = ""
        
        self.minWidth = 200
        self.minHeight = 100

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2c3e50"))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        self.container = QWidget(self)
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.container.setStyleSheet("""
            QWidget {
                border-radius: 15px;
                background-color: #333;
                color: #ecf0f1;
                border: 1px solid #3498db;
            }
        """)

        self.textBox = QTextEdit(self)
        self.textBox.setReadOnly(True)
        font = QFont("Arial", 24, QFont.Weight.Bold) 
        self.textBox.setCurrentFont(font)
        self.textBox.document().setDefaultFont(font)
        self.textBox.setStyleSheet("padding: 15px; border: none; background-color: #3498db; color: white;")
        self.textBox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout.addWidget(self.textBox)
        self.textToDisplay = ""
        
        self.nextButton = QPushButton("Next", self)
        self.nextButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        """)
        self.nextButton.setGeometry(0, self.height() - 100, self.width(), 70)
        self.nextButton.clicked.connect(self.onNextButtonClicked)


        self.animation = QPropertyAnimation(self.container, b"geometry")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setDuration(400)

        self.updateContainerGeometry()
        self.container.setGeometry(100, 100, self.minWidth, self.minHeight)

        self.loader = Loader()
        self.loader.setProject(filePath)
        self.loader.loadPackage()

        self.vm = ViewerVariableManager()
        self.files = FileManager()
        
        self.menuOverlay = SceneViewMenuOverlay(self.saveGame, self.loadGame, self)
        self.menuOverlay.setParent(self)
        self.menuOverlay.hide()
        self.menuOverlay.closeMenu.connect(self.toggleMenuOverlay)    
        
        if freshStart:
            self.loadScene(self.loader.getStartScene())
            self.adjustSizeToContent()
            self.container.show()
            self.running = True
            self.showingNext = True
       
    # SCENE PLAYER 
    
    def next(self):
        if self.currentLineIndex < len(self.script):  
            self.showingNext = True
            element = self.script[self.currentLineIndex]
            match element['type']:
                case "dialogue":
                    self.nextEntry['type'] = 'dialogue'
                    if element["speaker"]:
                        text = f"{element['speaker']}: {element['text']}"
                        self.setTextLetterByLetter(text)
                        self.nextEntry['speaker'] = element['speaker']
                        self.nextEntry['text'] = text
                        #self.textBox.setText(f'{element['speaker']}: "{element['text']}"')
                    else:
                        self.setTextLetterByLetter(f"{element['text']}")
                        self.nextEntry['text'] = element['text']
                        #self.textBox.setText(f"{element['text']}")
                    if "audio" in element:
                        self.audioPath = element["audio"]
                        self.nextEntry['audio'] = element["audio"]
                    QApplication.processEvents() 
                    self.adjustSizeToContent()
                    self.textBox.setFocus()
                case "choice":
                    self.nextEntry['type'] = 'choice'
                    # for i, choice in enumerate(element['choices']):
                    #     self.addButtonToTextBoxArea(
                    #         f"Option {i + 1}: {choice['text']}",
                    #         lambda index=i, cur=self.currentLineIndex: self.handleNewLines(cur, index)
                    #     )
                        
                    for i, choice in enumerate(element['choices']):
                        def makeHandler(index, curIndex):
                            return lambda: self.handleNewLines(curIndex, index)
                        handler = makeHandler(i, self.currentLineIndex)
                        self.addButtonToTextBoxArea(f"Option {i + 1}: {choice['text']}", handler)
                    
                    self.nextButton.hide()
                    self.showingNext = False
                case "conditional":
                    if eval(element["comparison"]):
                        self.conditionalsLog.append(1)
                        self.handleNewLines(self.currentLineIndex)
                    else:
                        self.conditionalsLog.append(0)
                        self.handleNewLines(self.currentLineIndex)
                case "modify":
                    eval(element['action'])
                    self.advanceScript()
                case "sfx":
                    self.playCurrentElementAudio()
                    self.advanceScript()
                case "bgm":
                    self.playCurrentElementAudio()
                    self.advanceScript()
                case "branch":
                    self.loadScene(element['next'])
                case "bg":
                    self.backgroundManager.setBackgroundFile(element['path'], self.loader.getPackagePath())
                    self.backgroundPath = element['path']
                    self.background.show()
                    self.advanceScript()
                case _:
                    print(element)
                    self.advanceScript()
        else:
            self.textBox.setText("The End")
            self.nextButton.setText("Close")
            self.running = False
            self.nextButton.clicked.connect(QApplication.quit)
        self.adjustSizeToContent()

    def playCurrentElementAudio(self):
        self.settings = UICustomizeDialog()
        volumes = self.settings.importVolumeDict()
        self.audio.changeVolumes(volumes)
        if self.currentLineIndex < len(self.script):
            element = self.script[self.currentLineIndex]
            if element['type'] == 'dialogue':
                self.audio.playDialogue(element['audio'], True, self.loader.getPackagePath())
            if element['type'] == 'sfx':
                self.audio.playSoundEffect(element['path'], True, self.loader.getPackagePath())
            if element['type'] == 'bgm':
                self.currentBGM = element['path']
                self.audio.playBackgroundMusic(element['path'], True, True, self.loader.getPackagePath())
    
    def loadScene(self, sceneName):
        self.sceneData = self.loader.readSceneToDict(sceneName)
        self.currentScene = sceneName
        self.choiceLog = []
        self.conditionalsLog = []
        self.script = self.sceneData['lines']        
        self.currentLineIndex = 0
        self.next()
        
    def advanceScript(self):
        self.currentLineIndex += 1
        self.next()
        self.updateDialogueHistory()

    def updateDialogueHistory(self):
        if bool(self.nextEntry):
            self.dialogueHistory.append(self.nextEntry.copy())
            if len(self.dialogueHistory) > 25:
                self.dialogueHistory.pop(0)
            self.nextEntry.clear()
    
    def getDialogueHistory(self):
        return self.dialogueHistory
    
    def onNextButtonClicked(self):
        if (self.running and self.script[self.currentLineIndex]['type'] != 'choice'):
            self.advanceScript()

    def handleNewLines(self, currentLineIndex, choiceIndex:int=-1, loading: bool= False):
        element = self.script[currentLineIndex]
        if 'text' in element:
            self.nextEntry['text'] = element['text']
        if element['type'] == 'choice':
            lines = element['choices'][choiceIndex]['lines']
        elif element['type'] == 'conditional':
            if eval(element["comparison"]):
                lines = element['ifLines']
            else:
                lines = element['elseLines']
        for button in self.container.findChildren(QPushButton):
            if button is not self.nextButton:
                self.showinNext = True
                self.nextButton.show()
                self.clearButtons()
                break
        for i in range(len(lines)-1,-1,-1):
            self.script.insert(self.currentLineIndex + 1, lines[i])
        if not loading:
            if choiceIndex != -1:
                self.choiceLog.append(choiceIndex)
            self.advanceScript()
    
    # Saves
    
    def saveGame(self):
        savefile = {}
        savefile['variables'] = self.vm.getVariables()
        time = datetime.now()
        savefile['date'] = str(time)
        savefile['currentScene'] = self.currentScene
        savefile['currentLineIndex'] = self.currentLineIndex
        savefile['choiceLog'] = self.choiceLog
        savefile['conditionalsLog'] = self.conditionalsLog
        savefile['dialogueHistory'] = self.dialogueHistory
        savefile['backgroundPath'] = self.backgroundPath
        savefile['currentBGM'] = self.currentBGM
        return savefile
    
    def loadGame(self, filepath: str):
        self.container.hide()
        self.background.hide()
        self.nextButton.hide()
        
        self.audio.stopBackgroundMusic()
        savedata = self.files.readSaveFile(filepath)
        if 'variables' in savedata:
            self.vm.loadFromDict(savedata['variables'])
        self.currentScene = savedata['currentScene']
        self.sceneData = self.loader.readSceneToDict(self.currentScene)
        self.script = self.sceneData['lines']        
        self.choiceLog = savedata['choiceLog']
        self.conditionalsLog = savedata['conditionalsLog']
        self.dialogueHistory = savedata['dialogueHistory']
        self.backgroundPath = savedata['backgroundPath']
        self.currentBGM = savedata['currentBGM']
        targetIndex = savedata['currentLineIndex']
        
        choiceLog = self.choiceLog.copy()   
        conditionalsLog = self.conditionalsLog.copy()
        
        self.currentLineIndex = 0
        while self.currentLineIndex <= targetIndex:
            self.showingNext = True
            element = self.script[self.currentLineIndex]
            match element['type']:
                case "dialogue":
                    self.nextEntry['type'] = 'dialogue'
                    if element["speaker"]:
                        text = f"{element['speaker']}: {element['text']}"
                        self.textBox.setText(text)
                        self.nextEntry['speaker'] = element['speaker']
                        self.nextEntry['text'] = text
                    else:
                        self.textBox.setText(f"{element['text']}")
                        self.nextEntry['text'] = element['text']
                    if "audio" in element:
                        self.audioPath = element["audio"]
                        self.nextEntry['audio'] = element["audio"]
                    QApplication.processEvents() 
                    self.adjustSizeToContent()
                    self.textBox.setFocus()
                case "choice":
                    self.nextEntry['type'] = 'choice'
                    if not choiceLog:
                        for i, choice in enumerate(element['choices']):
                            self.addButtonToTextBoxArea(
                                f"Option {i + 1}: {choice['text']}",
                                lambda index=i, cur=self.currentLineIndex: self.handleNewLines(cur, index, loading=True)
                            )
                        self.nextButton.hide()
                        self.showingNext = False
                    else:
                        for i, choice in enumerate(element['choices']):
                            if i == choiceLog[0]:
                                self.handleNewLines(self.currentLineIndex, i,loading=True)
                                choiceLog.pop(0)
                                break
                case "conditional":
                    if conditionalsLog[0] == 1:
                       self.handleNewLines(element["ifLines"], element, loading=True)
                    else:
                       self.handleNewLines(element["elseLines"], element ,loading=True)
                    conditionalsLog.pop(0)
                case _:
                    pass
            self.currentLineIndex += 1
            
        self.currentLineIndex -= 1
        if self.backgroundPath:
            self.backgroundManager.setBackgroundFile(self.backgroundPath, self.loader.getPackagePath())
            self.background.show()
        if self.currentBGM:
            self.audio.playBackgroundMusic(self.currentBGM, True, True, self.loader.getPackagePath())
        self.adjustSizeToContent()
        self.running = True
        self.container.show()
        if self.showingNext:
            self.nextButton.show()

        
        
    
    # UI
    
    def toggleMenuOverlay(self):
        if self.menuOverlay.isVisible():
            self.menuOverlay.hide()
            if self.showingNext:
                self.nextButton.show()
            self.container.show()  
        else:
            self.menuOverlay.setGeometry(self.rect())
            if self.showingNext:
                self.nextButton.hide()
            self.menuOverlay.raise_()
            self.menuOverlay.switchToPauseMenu()
            self.menuOverlay.move(self.rect().center() - self.menuOverlay.rect().center())
            self.menuOverlay.setFocus()
            self.menuOverlay.show()
            self.container.hide()

    def addButtonToTextBoxArea(self, buttonText="Button", onClick=None):
        newButton = QPushButton(buttonText, self.container)
        newButton.setStyleSheet("""
            QPushButton {
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
                                """)
        newButton.destroyed.connect(self.onButtonDeleted)
        font = QFont("Arial", 24)
        newButton.setFont(font)
        
        if onClick:
            newButton.clicked.connect(onClick)
            
        self.layout.addWidget(newButton)
        self.adjustSizeToContent()

    def clearButtons(self):
        for button in self.container.findChildren(QPushButton):
            if button is not self.nextButton:
                self.layout.removeWidget(button)
                button.deleteLater()

    def setTextLetterByLetter(self, text, interval=20):
        self.textToDisplay = text
        self.currentIndex = 0
        self.textBox.setText("")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateText)
        self.timer.start(interval)

    def updateText(self):
        if self.currentIndex < len(self.textToDisplay):
            self.textBox.setText(self.textToDisplay[:self.currentIndex + 1])
            self.currentIndex += 1
        else:
            self.timer.stop()  
    
    def onButtonDeleted(self):
        self.adjustSizeToContent()

    def adjustSizeToContent(self):
        document = self.textBox.document()
        if self.textToDisplay:
            document = document.clone()
            document.setPlainText(self.textToDisplay)
            
        maxWidth = self.width() * 0.5
        document.setTextWidth(maxWidth)

        contentSize = document.size()
        frameWidth = self.textBox.frameWidth()
        extraHeightPadding = 30
        totalPadding = frameWidth * 2 + extraHeightPadding
        newWidth = max(contentSize.width() + totalPadding, self.minWidth)
        
        newHeight = max(contentSize.height() + totalPadding, self.minHeight)
        buttonHeight = sum(button.sizeHint().height() for button in self.container.findChildren(QPushButton))
        totalHeight = newHeight + buttonHeight + (5 * len(self.container.findChildren(QPushButton)) - 15)
        
        startGeometry = self.container.geometry()
        endGeometry = QRect(
            int((self.width() - newWidth) // 2),
            int((self.height() - totalHeight) // 2),
            int(newWidth),
            int(totalHeight)
        )
        self.animation.setStartValue(startGeometry)
        self.animation.setEndValue(endGeometry)
        self.animation.start()

    def updateContainerGeometry(self):
        newX = (self.width() - self.container.width()) // 2
        newY = (self.height() - self.container.height()) // 2
        self.container.move(newX, newY)
    
    # Events
    
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustSizeToContent()
        self.updateContainerGeometry()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_M:
            self.toggleMenuOverlay()
        elif event.key() == Qt.Key_Z:
            if not self.menuOverlay.isVisible():
                self.nextButton.click()
        elif event.key() == Qt.Key_X:
            if not self.menuOverlay.isVisible():
                self.playCurrentElementAudio()
        elif event.key() == Qt.Key_P:
            self.saveGame()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        self.audio.cleanupTempFiles()
        super().closeEvent(event)
    
    
