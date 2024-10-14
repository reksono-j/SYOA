
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
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# play sound cure on start and stop recording
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

    @staticmethod
    def getOverlay():
        if STT.overlay is None:
            # overlay things
            STT.overlay = QWidget()
            STT.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
            STT.overlay.hide()
            STT.overlayText = QLabel("Some text idk", STT.overlay)
            STT.overlayText.setStyleSheet("color: white; font-size: 25px;")
            STT.overlayText.setAlignment(Qt.AlignCenter)
        else:
            return STT.overlay
    

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

        STT.getOverlay().setParent(activeWindow)
        STT.getOverlay().setGeometry(activeWindow.rect())
        STT.overlayText.setGeometry(activeWindow.rect())
        STT.getOverlay().show()

    @staticmethod
    def hideOverlay():
        STT.getOverlay().hide()

    @staticmethod
    def setOverlayText(s):
        if STT.overlay is None:
            STT.getOverlay() # just to initialize overlay and overlayText
        STT.overlayText.setText(s)
        
    