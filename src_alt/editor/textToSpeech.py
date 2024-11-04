"""
pip install torch torchaudio silero
"""

import torch
import torchaudio
import io
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


class VOICE(Enum):
    male1 = "en_7"
    male2 = "en_15"
    male3 = "en_17"
    male4 = "en_19"
    male5 = "en_20"
    female1 = "en_0"
    female2 = "en_3"
    female3 = "en_5"
    female4 = "en_11"
    female5 = "en_14"

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
    def convertToAudio(text: str):
        audio = TTS.model.apply_tts(text=text,  
                                speaker=TTS.speaker,
                                sample_rate=TTS.sample_rate)
        audio = audio.unsqueeze(0)

        audioBuffer = io.BytesIO()
        torchaudio.save(audioBuffer, audio, TTS.sample_rate, format="wav")
        audioBuffer.seek(0) 
        return audioBuffer
    
    @staticmethod
    def convertToAudioSSML(SSMLObj:SSMLBuilder):
        if(isinstance(SSMLObj, SSMLBuilder)):
            ssmlText = SSMLObj.getSSMLText()

            print(TTS.speaker)

            audio = TTS.model.apply_tts(ssml_text=ssmlText,
                                speaker=TTS.speaker,
                                sample_rate=TTS.sample_rate)
            audio = audio.unsqueeze(0)
            audioBuffer = io.BytesIO()
            torchaudio.save(audioBuffer, audio, TTS.sample_rate, format="wav")
            return audioBuffer
        else:
            print("You must pass in an SSMLBuilder object")
    
    @staticmethod
    def printSpeakers():
        print(TTS.model.speakers)

    @staticmethod
    def setSpeaker(speaker:VOICE):
        """
        valid speakers are en_0, en_1, ... en_117
        """
        if isinstance(speaker, VOICE):
            TTS.speaker = speaker.value
        else:
            print(f'in setSpeaker(), parameter must be of type VOICE')

        #if speakerString in TTS.model.speakers:
        #    TTS.speaker = speakerString
        #else:
        #    print(str(speakerString) + " is not a valid speaker")



if __name__ == '__main__':
    ssml = SSMLBuilder()
    ssml.addText("hello, what the hell are you doing?")
    ssml.addPause(500)
    ssml.addText("I have a question for you though", rate=RATE.xFast, pitch = PITCH.medium)
    

    audioBuffer = TTS.convertToAudioSSML(ssml)
    with open("female.mp3", "wb") as file:
        file.write(audioBuffer.getvalue())

    TTS.setSpeaker(VOICE.male1)
    audioBuffer = TTS.convertToAudioSSML(ssml)
    with open("male.mp3", "wb") as file:
        file.write(audioBuffer.getvalue())






