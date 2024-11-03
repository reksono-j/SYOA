from PySide6.QtWidgets import QApplication, QTextEdit, QMainWindow, QPushButton, QWidget, QVBoxLayout
from PySide6.QtCore import QRect, QPropertyAnimation, QEasingCurve, Qt, Signal, QTimer
from PySide6.QtGui import QFont, QPalette, QColor
import sys
from loader import Loader


class SceneView(QMainWindow):
    def __init__(self, filePath):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(1280, 720)
        
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
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #3498db;
            }
        """)

        self.textBox = QTextEdit(self)
        self.textBox.setReadOnly(True)
        font = QFont("Arial", 24, QFont.Weight.Bold) 
        self.textBox.document().setDefaultFont(font)
        self.textBox.setStyleSheet("padding: 15px; border: none; background-color: #3498db; color: white;")
        self.textBox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout.addWidget(self.textBox)


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
        self.loader.readStoryFilePaths()
        self.loadScene("Scene1") # TODO: Setup whatever the beginning script is.
        
        self.adjustSizeToContent()
        self.container.show()
        
    # SCENE PLAYER STUFF
    
    def next(self):
        if self.currentLineIndex < len(self.script):
            element = self.script[self.currentLineIndex]
            match element['type']:
                case "dialogue":
                    if element["speaker"]:
                        self.setTextLetterByLetter(f'{element['speaker']}: "{element['text']}"')
                        #self.textBox.setText(f'{element['speaker']}: "{element['text']}"')
                    else:
                        self.setTextLetterByLetter(f"{element['text']}")
                        #self.textBox.setText(f"{element['text']}")
                    if "audio" in element:
                        self.audioPath = element["audio"]
                    QApplication.processEvents() 
                    self.adjustSizeToContent()
                case "choice":
                    for i, choice in enumerate(element['choices']):
                        self.addButtonToTextBoxArea(f"Option {i + 1}: {choice['text']}", lambda: self.handleNewLines(choice['lines']))
                    self.nextButton.hide()
                case "modify":
                    # TODO: Add Variable Manager
                    self.advanceDialogue()
                case "conditional":
                    # TODO: Add Variable Manager
                    # if eval(element["comparison"]):
                    #   self.handleNewLines(element["ifLines"])
                    # else:
                    #   self.handleNewLines(element["ifLines"])
                    self.handleNewLines(element["ifLines"])
                case "branch":
                    self.loadScene(element['next'])
                case _:
                    print(element)
        else:
            self.textBox.setText("The End")
            self.nextButton.setText("Close")
            self.nextButton.clicked.disconnect()
            self.nextButton.clicked.connect(self.close)
        self.adjustSizeToContent()

    
    def loadScene(self, sceneName):
        self.sceneData = self.loader.readSceneToDict(sceneName)
        self.script = self.sceneData['lines']        
        self.currentLineIndex = 0
        self.next()
        self.adjustSize()
        
    def advanceDialogue(self):    
        self.currentLineIndex += 1
        self.next()
    
    def onNextButtonClicked(self):
        self.advanceDialogue()

    def handleNewLines(self, lines):
        for button in self.container.findChildren(QPushButton):
            if button is not self.nextButton:
                self.nextButton.show()
                self.clearButtons()
                break
        for line in lines:
            self.script.insert(self.currentLineIndex + 1, line)
        self.advanceDialogue()


    
    # UI STUFF
    
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

            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustSizeToContent()
        self.updateContainerGeometry()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = SceneView("SYOA/src_alt/viewer/Story_EX_DeleteLater/testStory.syoa")
    mainWindow.show()
    sys.exit(app.exec())
