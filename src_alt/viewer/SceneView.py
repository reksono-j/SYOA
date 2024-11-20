import sys, os
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QTextEdit, QMainWindow, QPushButton, 
    QWidget, QVBoxLayout, QDialog, QStackedWidget, QLabel,
    QScrollArea, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import QRect, QPropertyAnimation, QEasingCurve, Qt, QTimer, Signal, QCoreApplication
from PySide6.QtGui import QFont, QPalette, QColor, QPainter, QPixmap
from loader import Loader
from audioManager import AudioManager
from variables import ViewerVariableManager
from files import FileManager

class DialogueLog(QWidget):
    def __init__(self):
        super().__init__()



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
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.setWindowFlags(Qt.FramelessWindowHint) 
        
        self.layout = QVBoxLayout(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)  

        self.menuStack = QStackedWidget()
        self.menuStack.setStyleSheet("background: transparent; border: none;")
        self.layout.addWidget(self.menuStack)

        self.pauseMenu = self.createPauseMenu()
        self.saveMenu = self.createSaveLoadMenu(isSaveMenu=True)
        self.loadMenu = self.createSaveLoadMenu(isSaveMenu=False)
        self.settingsMenu = self.createSettingsMenu()

        self.menuStack.addWidget(self.pauseMenu)
        self.menuStack.addWidget(self.saveMenu)
        self.menuStack.addWidget(self.loadMenu)
        self.menuStack.addWidget(self.settingsMenu)

        self.menuStack.setCurrentWidget(self.pauseMenu)
        
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
        settingsButton.clicked.connect(lambda: self.menuStack.setCurrentWidget(self.settingsMenu))
        quitButton.clicked.connect(QCoreApplication.quit)

        return menu

    def createSaveLoadMenu(self, isSaveMenu):
        menu = QWidget()
        layout = QVBoxLayout(menu)
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Save Menu" if isSaveMenu else "Load Menu")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; color: white; padding: 10px;")
        layout.addWidget(title)

        layout.setSpacing(20) 
        scrollArea = QScrollArea()
        scrollArea.setStyleSheet("""
            border-radius: 15px;
            background-color: #333;
            border: 1px solid #3498db;
        """)
        scrollArea.setWidgetResizable(True)
        
        # The scroll area will be where the saves are laid out
        slotContainer = QWidget()
        slotLayout = QVBoxLayout(slotContainer)

        for i in range(10):  
            slotWidget = QWidget()
            slotWidget.setStyleSheet("border: 1px solid #3498db;")
            slotLayoutRow = QHBoxLayout(slotWidget)
            slotLabel = QLabel(f"Slot {i+1} - Empty")  # TODO: Actually load saves
            slotLabel.setStyleSheet("color: white; font-size: 16px;")
            slotLayoutRow.addWidget(slotLabel)
            slotLayoutRow.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
            
            slotLayout.addWidget(slotWidget)

        slotContainer.setLayout(slotLayout)
        scrollArea.setWidget(slotContainer)
        layout.addWidget(scrollArea)

        backButton = QPushButton("Back")
        backButton.setStyleSheet(self.BUTTON_STYLE)
        backButton.clicked.connect(lambda: self.menuStack.setCurrentWidget(self.pauseMenu))
        layout.addWidget(backButton)
        menu.setLayout(layout)
        
        return menu 
      
    def createSettingsMenu(self):
        menu = QWidget()
        layout = QVBoxLayout(menu)
        layout.setAlignment(Qt.AlignCenter)

        warningLabel = QLabel("OUT OF ORDER")
        warningLabel.setStyleSheet("font-size: 32px; color: white;")
        layout.addWidget(warningLabel)

        backButton = QPushButton("Back")
        backButton.setStyleSheet(self.BUTTON_STYLE)
        backButton.clicked.connect(lambda: self.menuStack.setCurrentWidget(self.pauseMenu))
        layout.addWidget(backButton)

        return menu

class SceneViewBackground(QWidget):
    def __init__(self):
        super().__init__()
        self.background = QPixmap()
        
    def setBackground(self, filepath):
        if os.path.exists(filepath):
            self.background = QPixmap(filepath)
            if self.background.isNull():
                print(f"Failed to load image: {filepath}")
            self.update() 
        else:
            print(f"Image file not found: {filepath}")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background.isNull():
            aspectRatio = self.background.height() / self.background.width()
            newWidth = self.width() + 30
            newHeight = int(newWidth * aspectRatio)

            scaledPixmap = self.background.scaled(newWidth, newHeight, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            painter.drawPixmap((self.width() - scaledPixmap.width()) // 2 - 15, 
                               (self.height() - scaledPixmap.height()) // 2 - 15, 
                               scaledPixmap)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()
        
class SceneView(QMainWindow):
    def __init__(self, filePath, freshStart):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(1280, 720)
                
        self.audio = AudioManager()
        
        self.background = SceneViewBackground()
        self.background.setBackground('grid.jpg')
        self.setCentralWidget(self.background)
        self.background.setGeometry(self.rect())
        #self.background.show()
        
        self.dialogueHistory = []
        self.nextEntry = {}
        
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

        self.menuOverlay = SceneViewMenuOverlay()
        self.menuOverlay.setParent(self)
        self.menuOverlay.hide()
        self.menuOverlay.closeMenu.connect(self.toggleMenuOverlay)    
        
        self.loader = Loader()
        self.loader.setProject(filePath)
        self.loader.loadPackage()

        self.vm = ViewerVariableManager()
        self.files = FileManager()
        
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
                        text = f'{element['speaker']}: "{element['text']}"'
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
                    for i, choice in enumerate(element['choices']):
                        self.addButtonToTextBoxArea(f"Option {i + 1}: {choice['text']}", lambda: self.handleNewLines(choice['lines'], element, choice['index']))
                    self.nextButton.hide()
                    self.showingNext = False
                case "conditional":
                    if eval(element["comparison"]):
                       self.handleNewLines(element["ifLines"], element)
                       self.conditionalsLog.append(1)
                    else:
                       self.handleNewLines(element["elseLines"], element)
                       self.conditionalsLog.append(0)
                    self.handleNewLines(element["ifLines"], element)
                case "modify":
                    eval(element['action'])
                    self.advanceScript()
                case "sfx":
                    self.playCurrentElementAudio(self)
                    self.advanceScript()
                case "bgm":
                    self.playCurrentElementAudio(self)
                    self.advanceScript()
                case "branch":
                    self.loadScene(element['next'])
                case "background": # TODO
                    pass 
                case _:
                    print(element)
        else:
            self.textBox.setText("The End")
            self.nextButton.setText("Close")
            self.running = False
            self.nextButton.clicked.connect(QApplication.quit)
        self.adjustSizeToContent()

    def playCurrentElementAudio(self):
        if self.currentLineIndex < len(self.script):
            element = self.script[self.currentLineIndex]
            if 'audio' in element:
                if element['type'] == 'dialogue':
                    self.audio.playDialogue(element['audio'], True, self.loader.getPackagePath())
                if element['type'] == 'sfx':
                    self.audio.playSoundEffect(element['audio'], True, self.loader.getPackagePath())
                if element['type'] == 'bgm':
                    self.audio.playBackgroundMusic(element['audio'], True, self.loader.getPackagePath())
    
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
        self.UpdateDialogueHistory()
        self.next()

    def UpdateDialogueHistory(self):
        if bool(self.nextEntry):
            self.dialogueHistory.append(self.nextEntry.copy())
            if len(self.dialogueHistory) > 25:
                self.dialogueHistory.pop(0)
            self.nextEntry.clear()
        
    # prospective log of all previously played lines
    # def updateLog(self):
    #    self.lineLog.append([self.currentScene, self.currentLineIndex])

    def onNextButtonClicked(self):
        if (self.running and self.script[self.currentLineIndex]['type'] != 'choice'):
            self.advanceScript()

    def handleNewLines(self, lines, element, choiceIndex:int=-1, loading: bool= False):
        if 'text' in element:
            self.nextEntry['text'] = element['text']
        for button in self.container.findChildren(QPushButton):
            if button is not self.nextButton:
                self.showinNext = True
                self.nextButton.show()
                self.clearButtons()
                break
        for line in lines:
            self.script.insert(self.currentLineIndex + 1, line)
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
        filename = time.strftime("save_%Y_%m_%d_%H_%M_%S")
        self.files.createSaveFile(filename, savefile)
    
    def loadGame(self, filepath: str):
        self.container.hide()
        self.nextButton.hide()
        
        
        savedata = self.files.readSaveFile(filepath)
        self.vm.loadFromDict(savedata['variables'])
        self.currentScene = savedata['currentScene']
        self.sceneData = self.loader.readSceneToDict(self.currentScene)
        self.script = self.sceneData['lines']        
        self.choiceLog = savedata['choiceLog']
        self.conditionalsLog = savedata['conditionalsLog']
        self.dialogueHistory = savedata['dialogueHistory']
        targetIndex = savedata['currentLineIndex']
        
        choiceLog = self.choiceLog.copy()   
        conditionalsLog = self.conditionalsLog.copy()
        
        self.currentLineIndex = 0
        while self.currentLineIndex < targetIndex:
            self.showingNext = True
            element = self.script[self.currentLineIndex]
            match element['type']:
                case "dialogue":
                    self.nextEntry['type'] = 'dialogue'
                    if element["speaker"]:
                        text = f'{element['speaker']}: "{element['text']}"'
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
                            self.addButtonToTextBoxArea(f"Option {i + 1}: {choice['text']}", lambda: self.handleNewLines(choice['lines'], element, choice['index']))
                        self.nextButton.hide()
                        self.showingNext = False
                    else:
                        for choice in element['choices']:
                            if choice['index'] == choiceLog[0]:
                                self.handleNewLines(choice['lines'], element, choice['index'],loading=True)
                                choiceLog.pop(0)
                case "conditional":
                    if conditionalsLog[0] == 1:
                       self.handleNewLines(element["ifLines"], element, loading=True)
                    else:
                       self.handleNewLines(element["elseLines"], element ,loading=True)
                    conditionalsLog.pop(0)
                case _:
                    pass
            self.currentLineIndex += 1
        
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
        
    def exampleButtonAction(self):
        print("Button clicked!")

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


