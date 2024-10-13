
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
import keybinds
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import *


class STT():
    audio_model = whisper.load_model("tiny") # load Whisper model 

    audio_queue = queue.Queue() # put raw bytes in here
    recognizer = sr.Recognizer()
    source = sr.Microphone(sample_rate=16000) # the microphone
    with source:
        recognizer.adjust_for_ambient_noise(source)
    transcription = '' # the latest transcription
    currentlyRecording = False
    
    QApplication.activeWindow()

    # overlay things
    overlay = QWidget()
    overlay.setAccessibleName("Recording")
    overlay.setAccessibleDescription("Currently recording speech to text")
    overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
    overlay.hide()
    overlayText = QLabel("Some text idk", overlay)
    overlayText.setStyleSheet("color: white; font-size: 25px;")
    overlayText.setAlignment(Qt.AlignCenter)
    accessibleInterface = QAccessibleWidget(overlay, name="Recording", r=QAccessible.AlertMessage)

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
        STT.currentlyRecording = True
        print("Started Recording")
        STT.recordingThread.start()

        STT.setOverlayText("Recording")
        STT.showOverlay()


    @staticmethod
    def stopRecording():
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

        if isinstance(focused_widget, QTextEdit):
            if STT.currentlyRecording:
                STT.stopRecording()
            else:
                STT.startRecording()

            if(not STT.currentlyRecording):
                focused_widget.append(STT.getLatestTranscription())
        elif isinstance(focused_widget, QLineEdit):
            if STT.currentlyRecording:
                STT.stopRecording()
            else:
                STT.startRecording()

            if(not STT.currentlyRecording):
                focused_widget.setText(STT.getLatestTranscription())

    @staticmethod
    def showOverlay():
        activeWindow =  QApplication.activeWindow()

        STT.overlay.setParent(activeWindow)
        STT.overlay.setGeometry(activeWindow.rect())
        STT.overlayText.setGeometry(activeWindow.rect())
        STT.overlay.show()
        QAccessible.updateAccessibility(QAccessibleEvent(STT.overlay, QAccessible.Alert))

    @staticmethod
    def hideOverlay():
        QAccessible.updateAccessibility(QAccessibleEvent(STT.overlay, QAccessible.Alert))
        STT.overlay.hide()

    @staticmethod
    def setOverlayText(s):
        STT.overlayText.setText(s)
        
    