import unittest
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit
)
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
import json
import copy
import os
from pathlib import Path

from src_alt.editor import textToSpeech

class Test(unittest.TestCase):
    def setUp(self):
        self.TTS = textToSpeech.TTS

        workingDir = os.path.dirname(os.path.abspath(__file__))
        self.parent_path = os.path.dirname(workingDir)

    def tearDown(self):
        if os.path.exists(os.path.join(self.parent_path, 'test.mp3')):
            os.remove(os.path.join(self.parent_path, 'test.mp3'))
        if os.path.exists(os.path.join(self.parent_path, 'test1.mp3')):
            os.remove(os.path.join(self.parent_path, 'test1 .mp3'))
        return super().tearDown()
    

    def test_setSpeaker(self):
        self.TTS.setSpeaker("en_100")
        self.assertEqual(self.TTS.speaker, textToSpeech.VOICE.female1.value)

        self.TTS.setSpeaker(textToSpeech.VOICE.male1)
        self.assertEqual(self.TTS.speaker, textToSpeech.VOICE.male1.value)

        self.TTS.setSpeaker(textToSpeech.VOICE.male2)
        self.assertEqual(self.TTS.speaker, textToSpeech.VOICE.male2.value)

        self.TTS.setSpeaker(textToSpeech.VOICE.male3)
        self.assertEqual(self.TTS.speaker, textToSpeech.VOICE.male3.value)

    def test_ssml(self):
        ssmlBuilder = textToSpeech.SSMLBuilder()

        ssmlBuilder.addText("newText", rate=1, pitch=1)
        self.assertEqual(ssmlBuilder.getSSMLText().replace('\n',''), "<speak>newText</speak>")

        ssmlBuilder.addPause(500)
        self.assertEqual(ssmlBuilder.getSSMLText().replace('\n',''), '<speak>newText<break time="500ms"/></speak>')

        ssmlBuilder.addText("newText2", rate=textToSpeech.RATE.fast)
        self.assertEqual(ssmlBuilder.getSSMLText().replace('\n',''), '<speak>newText<break time="500ms"/><prosody rate="fast">newText2</prosody></speak>')

        ssmlBuilder.addText("newText2", pitch=textToSpeech.PITCH.high)
        self.assertEqual(ssmlBuilder.getSSMLText().replace('\n',''), '<speak>newText<break time="500ms"/><prosody rate="fast">newText2</prosody><prosody pitch="high">newText2</prosody></speak>')

    def test_createAudio(self):
        audioData = self.TTS.convertToAudio("Hello")
        with open("test.mp3", "wb") as file:
            file.write(audioData.getvalue())

        
        filePath = os.path.join(self.parent_path, 'test.mp3')
        self.assertTrue(os.path.exists(filePath))

        ssml = textToSpeech.SSMLBuilder()
        ssml.addText("hello",rate=textToSpeech.RATE.xFast)
        audioData = self.TTS.convertToAudioSSML(ssml)
        with open("test1.mp3", "wb") as file:
            file.write(audioData.getvalue())
        
        filePath = os.path.join(self.parent_path, 'test1.mp3')
        self.assertTrue(os.path.exists(filePath))


