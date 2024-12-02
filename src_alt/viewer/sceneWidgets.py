from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6 import *
        
class DialogueWidget(QLabel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet("margin: 0;")

        if isinstance(data, dict):
            if data["speaker"]:
                self.setText(f"{data['speaker']} says {data['text']}")
            else:
                self.setText(f"{data['text']}")
            self.audioPath = data["audio"]
        elif isinstance(data, str):
            self.setText(data)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.setStyleSheet("background-color: lightblue; padding: 5px;")

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.setStyleSheet("background-color: none; padding: 5px;")

class ChoiceWidget(QWidget):
    def __init__(self, data, handleChoice, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.buttons = []

        for i, choice in enumerate(data['choices']):
            button = NonActivatableButton(choice['text'])
            button.setAccessibleName(f"Option {i + 1}: {choice['text']}")
            button.setFocusPolicy(Qt.StrongFocus)
            button.clicked.connect(lambda: self.onChoiceButtonClicked(choice['lines'], handleChoice))
            self.layout.addWidget(button)
            self.buttons.append(button)

        self.setLayout(self.layout)

    def focusInEvent(self, event):
        super().focusOutEvent(event)
        self.promptLabel.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            focused_widget = self.focusWidget()
            if isinstance(focused_widget, NonActivatableButton):
                if focused_widget.active:
                    focused_widget.click()
            elif isinstance(focused_widget, NonActivatableButton):
                event.ignore()

    def onChoiceButtonClicked(self, consequences : list, handleChoice):
        for btn in self.buttons:
            btn.setActive(False)
        # button = self.sender()
        # selectedOption = button.text()
        # self.responseLabel = FocusableLabel(f"You selected {selectedOption}")
        # self.layout.addWidget(self.responseLabel)
        # self.responseLabel.setFocus()
        handleChoice(consequences)

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