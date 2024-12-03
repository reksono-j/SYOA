from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPixmap
import zipfile, tempfile
import os, atexit, time
from singleton import Singleton

class SceneViewBackground(QWidget):
    def __init__(self):
        super().__init__()
        self.background = QPixmap()
        
    def setBackground(self, filepath):
        if os.path.exists(filepath):
            self.background = QPixmap(filepath)
            if self.background.isNull():
                print(f"Failed to load image: {filepath}")
            self.update() 
        else:
            print(f"Image file not found: {filepath}")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background.isNull():
            aspectRatio = self.background.height() / self.background.width()
            newWidth = self.width() + 30
            newHeight = int(newWidth * aspectRatio)

            scaledPixmap = self.background.scaled(newWidth, newHeight, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            painter.drawPixmap((self.width() - scaledPixmap.width()) // 2 - 15, 
                               (self.height() - scaledPixmap.height()) // 2 - 15, 
                               scaledPixmap)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

class BackgroundManager(metaclass=Singleton):
    def __init__(self):
        self.background = SceneViewBackground()
        self.tempFiles = {}
    

    def getBackground(self):
        return self.background
    
    def _extractToTempFile(self, zipPath, backgroundPath):
        if backgroundPath in self.tempFiles:
            return self.tempFiles[backgroundPath]
        try:
            with zipfile.ZipFile(zipPath, 'r') as zipFile:
                if backgroundPath in zipFile.namelist():
                    tempFile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                    with zipFile.open(backgroundPath) as source, open(tempFile.name, 'wb') as target:
                        target.write(source.read())
                    self.tempFiles[backgroundPath] = tempFile.name
                    return tempFile.name
                else:
                    print(f"background file {backgroundPath} not found in zip.")
                    return None
        except Exception as e:
            print(f"Error extracting background to temp file: {e}")
            return None

    def setBackgroundFile(self, backgroundPath, zipPath=''):
        tempPath = self._extractToTempFile(zipPath, backgroundPath)
        if tempPath:
            self.background.setBackground(tempPath)
        else:
            print("Failed to load background from zip.")
            return