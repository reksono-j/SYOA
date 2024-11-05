import pyaudio
import threading
import os
from pydub import AudioSegment
import math
import multiprocessing
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit, QGridLayout,
)
import sys


def volumeLevelToDecibels(volumeLevel):
    if volumeLevel <= 0:
        return -70 
    elif volumeLevel >= 100:
        return 0
    else:
        return 20 * math.log10(volumeLevel / 100)

def playMP3(fileName:str, volume:int = 100):
    """
    volume: 0 to 100
    """
    if(volume>100 or volume<0):
        volume = 100

    workingDir = os.path.dirname(os.path.abspath(__file__))
    trueFilePath = os.path.join(workingDir, "audio", fileName)

    audio = AudioSegment.from_mp3(trueFilePath)
    audio = audio.apply_gain(volumeLevelToDecibels(volume))

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(audio.sample_width),
                    channels=audio.channels,
                    rate=audio.frame_rate,
                    output=True)

    raw_data = audio.raw_data

    chunk_size = 1024
    for i in range(0, len(raw_data), chunk_size):
        stream.write(raw_data[i:i + chunk_size])

    stream.stop_stream()
    stream.close()
    p.terminate()


def playMP3inThread(fileName:str, volume:int = 100):
    """
    volume: 0 to 100
    Seems to crash with speechToText, so do not use
    """
    audioThread = threading.Thread(target = (lambda fn=fileName, v=volume: playMP3(fn, v)))
    audioThread.start()

def addAudioToQueue(queue, fileName, volume=100):
    queue.put((fileName, volume))

class AudioPlayer():
    _queue = None
    _process = None

    #@staticmethod
    #def _audioPlaybackWorker(queue: multiprocessing.Queue):
    #    p = pyaudio.PyAudio()
#
    #    try:
    #        while True:
    #            item = queue.get()
    #            
    #            filePath, volume = item
#
    #            audio = AudioSegment.from_mp3(filePath)
    #            audio = audio.apply_gain(volumeLevelToDecibels(volume))
#
    #            stream = p.open(format=p.get_format_from_width(audio.sample_width),
    #                            channels=audio.channels,
    #                            rate=audio.frame_rate,
    #                            output=True)
#
    #            raw_data = audio.raw_data
    #            chunk_size = 1024
    #            for i in range(0, len(raw_data), chunk_size):
    #                stream.write(raw_data[i:i + chunk_size])
#
    #            stream.stop_stream()
    #            stream.close()
    #    
    #    finally:
    #        p.terminate()

    def _audioPlaybackWorker(queue: multiprocessing.Queue):
        p = pyaudio.PyAudio()

        try:
            while True:
                try:
                    item = queue.get()
                    filePath, volume = item
                    audio = AudioSegment.from_mp3(filePath)

                    volume_db = volumeLevelToDecibels(volume)
                    audio = audio.apply_gain(volume_db)

                    stream = p.open(format=p.get_format_from_width(audio.sample_width),
                                    channels=audio.channels,
                                    rate=audio.frame_rate,
                                    output=True)

                    raw_data = audio.raw_data
                    chunk_size = 1024
                    for i in range(0, len(raw_data), chunk_size):
                        stream.write(raw_data[i:i + chunk_size])

                    stream.stop_stream()
                    stream.close()

                except Exception as e:
                    print(f"Error while playing audio: {e}")

        finally:
            p.terminate()

    @staticmethod
    def _initialize():
        AudioPlayer._queue = multiprocessing.Queue()
        AudioPlayer._process = multiprocessing.Process(target=AudioPlayer._audioPlaybackWorker, args=(AudioPlayer._queue,))
        AudioPlayer._process.start()

    @staticmethod
    def playMP3(filePath:str, volume:int = 100):
        """
        filePath must be the whole path.
        Use: 
            workingDir = os.path.dirname(os.path.abspath(__file__))
            trueFilePath = os.path.join(workingDir, "audio", someFileName)
        """
        if AudioPlayer._queue is None:
            AudioPlayer._initialize()

        if(volume>100 or volume<0): volume=100
        
        AudioPlayer._queue.put((filePath, volume))

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

            self.button = QPushButton("some button", self)
            self.button.clicked.connect(self.buttonFunc)
            layout.addWidget(self.button)

            central_widget.setLayout(layout)

        def buttonFunc(self):
            AudioPlayer.playMP3("recording.mp3")

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()


    sys.exit(app.exec())
