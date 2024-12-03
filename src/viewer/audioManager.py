from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QTimer
import zipfile, tempfile
import os, atexit, time
from src.viewer.singleton import Singleton

class AudioManager(metaclass=Singleton):
    def __init__(self):
        if not hasattr(self, "backgroundPlayer"):
            self.backgroundPlayer = QMediaPlayer()
            self.backgroundOutput = QAudioOutput()
            self.backgroundPlayer.setAudioOutput(self.backgroundOutput)

            self.dialoguePlayer = QMediaPlayer()
            self.dialogueOutput = QAudioOutput()
            self.dialoguePlayer.setAudioOutput(self.dialogueOutput)

            self.soundEffectPlayers = []  # List to hold SFX media players
            self.soundEffectOutputs = []
            self.tempFiles = {} 

            atexit.register(self.cleanupTempFiles)

    def _extractToTempFile(self, zipPath, audioPath):
        if audioPath in self.tempFiles:
            return self.tempFiles[audioPath]
        try:
            with zipfile.ZipFile(zipPath, 'r') as zipFile:
                if audioPath in zipFile.namelist():
                    tempFile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    with zipFile.open(audioPath) as source, open(tempFile.name, 'wb') as target:
                        target.write(source.read())
                    self.tempFiles[audioPath] = tempFile.name
                    return tempFile.name
                else:
                    print(f"Audio file {audioPath} not found in zip.")
                    return None
        except Exception as e:
            print(f"Error extracting audio to temp file: {e}")
            return None

    def getAudioFile(self, audioPath, player: QMediaPlayer, fromZip=False, zipPath=''):
        if fromZip:
            tempPath = self._extractToTempFile(zipPath, audioPath)
            if tempPath:
                player.setSource(QUrl.fromLocalFile(tempPath))
            else:
                print("Failed to load audio from zip.")
                return
        else:
            player.setSource(QUrl.fromLocalFile(audioPath))

    def playBackgroundMusic(self, audioPath, loop=True, fromZip=False, zipPath=''):
        self.backgroundPlayer.stop()
        self.getAudioFile(audioPath, self.backgroundPlayer, fromZip, zipPath)
        self.backgroundPlayer.setLoops(QMediaPlayer.Loops.Infinite if loop else 1)
        self.backgroundPlayer.play()

    def stopBackgroundMusic(self):
        self.backgroundPlayer.stop()

    def playDialogue(self, audioPath, fromZip=False, zipPath=''):
        self.dialoguePlayer.stop()
        self.getAudioFile(audioPath, self.dialoguePlayer, fromZip, zipPath)
        self.dialoguePlayer.setLoops(1)
        self.dialoguePlayer.play()

    def playSoundEffect(self, audioPath, fromZip=False, zipPath=''):
        player = QMediaPlayer()
        audioOutput = QAudioOutput()
        player.setAudioOutput(audioOutput)
        self.getAudioFile(audioPath, player, fromZip, zipPath)
        self.soundEffectPlayers.append(player)
        self.soundEffectOutputs.append(audioOutput)
        player.play()



    def cleanupTempFiles(self):
        if self.backgroundPlayer.mediaStatus() not in (QMediaPlayer.EndOfMedia, QMediaPlayer.NoMedia):
            self.backgroundPlayer.stop()
        if self.dialoguePlayer.mediaStatus() not in (QMediaPlayer.EndOfMedia, QMediaPlayer.NoMedia):
            self.dialoguePlayer.stop()
        self.backgroundPlayer.setSource(QUrl())
        self.dialoguePlayer.setSource(QUrl())
        for output in self.dialogueOutput:
            output.deleteLater()
        for player in self.soundEffectPlayers:
            player.stop()
            player.setSource(QUrl())
            player.deleteLater()
        QTimer.singleShot(100, self._deleteTempFiles)
        
    def _deleteTempFiles(self):
        time.sleep(0.1)
        for tempFile in set(self.tempFiles.values()):
            try:
                os.unlink(tempFile)
                print(f"Deleted temp file: {tempFile}")
            except Exception as e:
                print(f"Error deleting temp file {tempFile}: {e}")
        self.tempFiles.clear()