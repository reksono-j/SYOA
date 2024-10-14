"""
pip install torch torchaudio silero
"""

import torch
import torchaudio
from enum import Enum

class RATE(Enum):
    xSlow = "x-slow"
    slow = "slow"
    medium = "medium"
    fast = "fast"
    xFast = "x-fast"

class PITCH(Enum):
    xLow = "x-low"
    low = "low"
    medium = "medium"
    high = "high"
    xHigh = "x-high"

class SSMLBuilder():
    def __init__(self) -> None:
        self.SSMLText = '<speak>\n'  
        self.markupStack = ['</speak>']
    
    def addText(self, text:str, rate:RATE=None, pitch:PITCH=None):
        """
        example: SSMLBuilderObj.addText("some text", rate=RATE.fast, pitch=PITCH.high)
        example: SSMLBuilderObj.addText("some text")

        if you do not use the Enum, the text will be added to the SSML gracefully but invalid rate or pitch will have no effects.
        """

        if(rate==None and pitch==None):
            self.SSMLText += text
        else:
            appendToSSML = ["\n<prosody"]

            hasProperRateOrPitch = False

            if(isinstance(rate, RATE)):
                hasProperRateOrPitch = True
                appendToSSML.append(f' rate="{rate.value}"')
            if(isinstance(pitch, PITCH)):
                hasProperRateOrPitch = True
                appendToSSML.append(f' pitch="{pitch.value}"')
            
            if(hasProperRateOrPitch):
                appendToSSML.append(f'>{text}</prosody>')
            else:
                appendToSSML = [f'\n{text}']

            self.SSMLText += "".join(appendToSSML)
            
    def getSSMLText(self):
        return self.SSMLText + '\n</speak>'
    
    def addPause(self,milliseconds:int):
        self.SSMLText += f'\n<break time="{milliseconds}ms"/>'
    
class TTS():
    language = 'en'
    model_id = 'v3_en'
    device = torch.device('cpu')

    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                         model='silero_tts',
                                         language=language,
                                         speaker=model_id)
    model.to(device)

    sample_rate = 48000
    speaker = 'en_0' # which voice to use
    put_accent=True
    put_yo=True

    @staticmethod
    def convertToAudio(text:str, filePath):
        """
        example: TTS.convertToAudio("hello, my name is Don Chen","someAudio.wav")
        """
        audio = TTS.model.apply_tts(text=text,
                            speaker=TTS.speaker,
                            sample_rate=TTS.sample_rate)
        audio = audio.unsqueeze(0)
        torchaudio.save(filePath, audio, TTS.sample_rate)
    
    @staticmethod
    def convertToAudioSSML(SSMLObj:SSMLBuilder, filePath):
        if(isinstance(SSMLObj, SSMLBuilder)):
            ssmlText = SSMLObj.getSSMLText()

            audio = TTS.model.apply_tts(ssml_text=ssmlText,
                                speaker=TTS.speaker,
                                sample_rate=TTS.sample_rate)
            audio = audio.unsqueeze(0)
            torchaudio.save(filePath, audio, TTS.sample_rate)
        else:
            print("You must pass in an SSMLBuilder object")
    
    @staticmethod
    def printSpeakers():
        print(TTS.model.speakers)

    @staticmethod
    def setSpeaker(speakerString):
        """
        valid speakers are en_0, en_1, ... en_117
        """
        if speakerString in TTS.model.speakers:
            TTS.speaker = speakerString
        else:
            print(str(speakerString) + " is not a valid speaker")


#ssml = SSMLBuilder()
#ssml.addText("hello, what the hell are you doing?")
#ssml.addPause(500)
#ssml.addText("I have a question for you though", rate=RATE.xFast, pitch = PITCH.medium)
#
#TTS.convertToAudioSSML(ssml, "wave.wav")







