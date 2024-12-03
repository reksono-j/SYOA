import pyaudio
import threading
import os
from pydub import AudioSegment
import math


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
    """
    audioThread = threading.Thread(target = (lambda fn=fileName, v=volume: playMP3(fn, v)))
    audioThread.start()

if __name__ == "__main__":
    playMP3inThread('recording.mp3')
    for i in range(10):
        print(i)
