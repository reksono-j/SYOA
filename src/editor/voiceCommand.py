from src.editor.speechToText import *
from src.editor.keybinds import *
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeyEvent, QKeySequence


class VCManager():
    STT = STT
    shortcutsManager = ShortcutsManager.getInstance()
    mainWindow = shortcutsManager.window

    @staticmethod
    def simulateKeySequence(key_sequence:QKeySequence):
        event = QKeyEvent(QEvent.KeyPress, key_sequence.key(), Qt.NoModifier, key_sequence.text())
        QApplication.sendEvent(VCManager.mainWindow, event)

    @staticmethod
    def VCCallback():
        if VCManager.STT.currentlyRecording:
            VCManager.STT.stopRecording()
        else:
            VCManager.STT.startRecording()

        if(not VCManager.STT.currentlyRecording):
                # do stuff here
                print(VCManager.STT.getLatestTranscription())
                shortcutStr = VCManager.STT.getLatestTranscription()
                shortcutStr = shortcutStr.lower()
                shortcutStr = shortcutStr.replace(",", "").replace(".", "")
                shortcut = VCManager.shortcutsManager.shortcutDict.get(shortcutStr)

                if(shortcut is not None):
                    keySequence = shortcut.key()
                    print(keySequence)
                    VCManager.simulateKeySequence(keySequence)
                else:
                    print("shortcut does not exist: " + shortcutStr)
    
    shortcutsManager.addShortcut("v", "Voice Command", VCCallback)





