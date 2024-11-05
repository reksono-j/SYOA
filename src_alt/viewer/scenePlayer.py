import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from sceneWidgets import DialogueWidget, ChoiceWidget
from loader import Loader
from audioManager import AudioManager

class ScenePlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        
        self.audioManager = AudioManager()
        
        self.loader = Loader()
        self.loader.setProject("SYOA/src/viewer/Story_EX_DeleteLater/testStory.syoa") # TODO: setup to take a project path
        self.loader.readStoryFilePaths()
        self.loadScene("Scene1")
        self.setLayout(self.layout)
        self.show()

    def next(self):
        if self.currentLineIndex < len(self.script):
            element = self.script[self.currentLineIndex]
            match element['type']:
                case "dialogue":
                    dialogueWidget = DialogueWidget(element)
                    dialogueWidget.setFocusPolicy(Qt.StrongFocus)
                    self.layout.addWidget(dialogueWidget)    
                    
                    nextButton = QPushButton("Next")
                    nextButton.setDefault(True)
                    nextButton.setAccessibleName("Next")
                    nextButton.clicked.connect(lambda: self.onNextButtonClicked(nextButton))
                    self.layout.addWidget(nextButton)  
                    
                    QApplication.processEvents() 
                    dialogueWidget.setFocus()
                case "choice":
                    choiceWidget = ChoiceWidget(element, self.handleNewLines)
                    self.layout.addWidget(choiceWidget)
                    if len(choiceWidget.buttons) > 0:
                        choiceWidget.buttons[0].setFocus()
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
            print("SCRIPT OVER") # TODO

    
    def loadScene(self, sceneName):
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            self.layout.removeItem(item) 
        self.sceneData = self.loader.readSceneToDict(sceneName)
        self.script = self.sceneData['lines']        
        self.currentLineIndex = 0
        self.next()
        self.adjustSize()
        
    def advanceDialogue(self):    
        self.currentLineIndex += 1
        self.next()
    
    def onNextButtonClicked(self, button):
        self.layout.removeWidget(button)
        button.deleteLater()
        self.advanceDialogue()

    def handleNewLines(self, lines):
        for line in lines:
            self.script.insert(self.currentLineIndex + 1, line)
        self.advanceDialogue()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScenePlayer()
    window.show()
    sys.exit(app.exec())