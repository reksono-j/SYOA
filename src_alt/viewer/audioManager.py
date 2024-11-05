from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
from singleton import Singleton

class AudioManager(metaclass=Singleton):
    def __init__(self):
        if not hasattr(self, "backgroundPlayer"):
            # In PyQt, each of the mediaplayers can only play a single sound. 
            # There should be neither multiple background songs nor multiple dialogue tracks
            self.backgroundPlayer = QMediaPlayer()
            self.backgroundOutput = QAudioOutput()
            self.backgroundPlayer.setAudioOutput(self.backgroundOutput)
            
            self.dialoguePlayer = QMediaPlayer()
            self.dialogueOutput = QAudioOutput()
            self.dialoguePlayer.setAudioOutput(self.dialogueOutput)

            self.soundEffectPlayers = [] # List to hold SFX media players

    def playBackgroundMusic(self, audioPath, loop=True):
        self.backgroundPlayer.stop()
        self.backgroundPlayer.setSource(QUrl.fromLocalFile(audioPath))
        self.backgroundPlayer.setLoops(QMediaPlayer.Loops.Infinite if loop else 1)
        self.backgroundPlayer.play()

    def stopBackgroundMusic(self):
        self.backgroundPlayer.stop()

    def playDialogue(self, audioPath):
        self.dialoguePlayer.stop()
        self.dialoguePlayer.setSource(QUrl.fromLocalFile(audioPath))
        self.dialoguePlayer.setLoops(1)
        self.dialoguePlayer.play()

    def playSoundEffect(self, audioPath):
        player = QMediaPlayer()
        audioOutput = QAudioOutput()
        player.setAudioOutput(audioOutput)
        player.setSource(QUrl.fromLocalFile(audioPath))
        
        player.play()
        self.soundEffectPlayers.append(player)
        player.mediaStatusChanged.connect(lambda status: self.cleanupSoundEffect(player, status))

    def cleanupSoundEffect(self, player, status):
        if status == QMediaPlayer.EndOfMedia:
            self.soundEffectPlayers.remove(player)
            player.deleteLater() 
