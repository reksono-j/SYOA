
"""
Install these lirbaries below (run in terminal):
pip install torch openai-whisper SpeechRecognition numpy
"""

import whisper
import speech_recognition as sr
import numpy as np
import torch
import queue
import threading
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit, QPlainTextEdit
)
from PySide6.QtGui import Qt
from audioPlayer import AudioPlayer
import sys
import os



class STT():
    audio_model = whisper.load_model("tiny") # load Whisper model 

    audio_queue = queue.Queue() # put raw bytes in here
    recognizer = sr.Recognizer()
    source = sr.Microphone(sample_rate=16000) # the microphone
    with source:
        recognizer.adjust_for_ambient_noise(source)
    transcription = '' # the latest transcription
    currentlyRecording = False

    overlay = None
    overlayText = None
    stopButton = None


    workingDir = os.path.dirname(os.path.abspath(__file__))
    _recordingSoundPath = os.path.join(workingDir, "audio", "recording.mp3")
    _doneRecordingSoundPath = os.path.join(workingDir, "audio", "doneRecording.mp3")
    _volume = 100

    _textboxWidget = None

    @staticmethod
    def initializeWidgets():
        STT.overlay = QWidget()
        STT.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
        STT.overlay.hide()

        STT.overlayText = QLabel("Some text idk", STT.overlay)
        STT.overlayText.setStyleSheet("color: white; font-size: 25px;")
        STT.overlayText.setAlignment(Qt.AlignCenter)

        STT.stopButton = QPushButton("Stop Recording")
        STT.stopButton.setParent(STT.overlay)
        STT.stopButton.clicked.connect(STT.recordCallback)

        layout = QVBoxLayout()
        layout.addWidget(STT.overlayText)
        layout.addWidget(STT.stopButton)

        STT.overlay.setLayout(layout)
        STT.overlay.hide()

    @staticmethod
    def getOverlay():
        if STT.overlay is None:
            STT.initializeWidgets()
        
        return STT.overlay
    
    @staticmethod
    def getOverlayText():
        if STT.overlayText is None:
            STT.initializeWidgets()
        
        return STT.overlayText

    @staticmethod
    def recordAudioToQueue():
        with STT.source:
            while not STT.stopEvent.is_set():  # keep recording until stop event is set
                try:
                    audio_data = STT.recognizer.listen(STT.source, timeout=1)
                    STT.audio_queue.put(audio_data.get_raw_data())
                except sr.WaitTimeoutError: # not sure what this is
                    pass  
    
    @staticmethod
    def processAudioData():
        audioDataBytes = b''.join(STT.audio_queue.queue)
        STT.audio_queue.queue.clear()
        audioNDArray = np.frombuffer(audioDataBytes, dtype=np.int16).astype(np.float32) / 32768.0
        result = STT.audio_model.transcribe(audioNDArray, fp16=torch.cuda.is_available())
        STT.transcription = result['text'].strip()
        print(result['text'].strip())

    recordingThread = threading.Thread(target=recordAudioToQueue) # new thread to run recording function
    stopEvent = threading.Event()

    @staticmethod
    def startRecording():
        AudioPlayer.playMP3(STT._recordingSoundPath, STT._volume)

        STT.currentlyRecording = True
        print("Started Recording")
        STT.recordingThread.start()

        STT.setOverlayText("Recording")
        STT.showOverlay()

    @staticmethod
    def stopRecording():
        AudioPlayer.playMP3(STT._doneRecordingSoundPath, STT._volume)

        print("Stopped Recording")
        STT.currentlyRecording = False
        STT.stopEvent.set() # sets event usedd to stop recording function
        STT.recordingThread.join() # wait until recordingThread terminates
        STT.recordingThread = threading.Thread(target=STT.recordAudioToQueue) # reinitializes thread, to be able to start thread again
        STT.stopEvent.clear()


        # this does not update the text because processAudioData() is a long-running task that blocks GUI updates
        # using regular threads do not work
        # solution most likely QThread or just not having this
        STT.setOverlayText("Processing...") 


        STT.processAudioData()
        print("Finished processing")

        STT.hideOverlay()
        
    @staticmethod
    def getLatestTranscription():
        return STT.transcription
    
    @staticmethod
    def recordCallback():
        focused_widget = QApplication.focusWidget() # gets the focused widget, which should be the textbox

        if isinstance(focused_widget, QTextEdit) or isinstance(focused_widget, QLineEdit) or isinstance(focused_widget, QPlainTextEdit):
            STT._textboxWidget = focused_widget
        
        if STT.currentlyRecording:
            STT.stopRecording()
        else:
            STT.startRecording()
            
        if(not STT.currentlyRecording) and isinstance(STT._textboxWidget, QTextEdit):
            STT._textboxWidget.append(STT.getLatestTranscription())
        if(not STT.currentlyRecording) and isinstance(STT._textboxWidget, QLineEdit):
            STT._textboxWidget.setText(STT.getLatestTranscription())
        if(not STT.currentlyRecording) and isinstance(STT._textboxWidget, QPlainTextEdit):
            STT._textboxWidget.appendPlainText(STT.getLatestTranscription())

    @staticmethod
    def showOverlay():
        activeWindow =  QApplication.activeWindow()
        
        STT.getOverlay().setParent(activeWindow)
        STT.getOverlay().setGeometry(activeWindow.rect())
        STT.getOverlay().show()

    @staticmethod
    def hideOverlay():
        STT.getOverlay().hide()

    @staticmethod
    def setOverlayText(s):
        STT.getOverlayText().setText(s)



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

            self.button = QPushButton("some button1", self)
            self.button.clicked.connect(self.buttonFunc)
            layout.addWidget(self.button)

            shortcut = QShortcut(QKeySequence("Ctrl+k"), self)
            shortcut.activated.connect(STT.recordCallback)

            central_widget.setLayout(layout)

        def buttonFunc(self):
            STT.recordCallback()

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec())