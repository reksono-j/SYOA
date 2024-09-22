import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json

#Following same style as keybinds.py

class UICustomizeMenu(QGroupBox):
    def __init__(self, UICustomizeManager, parent):
        super(UICustomizeMenu, self).__init__(parent)
        self.parent = parent
        self.UICustomizeManager = UICustomizeManager

        #menu settings
        self.setTitle("UI Settings")
        self.setAlignment(2)
        self.setGeometry(0, 100, 1280, 700)

        #ui options boxes setup
        self.fontFamilyComboBox = QFontComboBox(self)

        self.fontSizeSpinBox = QSpinBox(self)
        self.fontSizeSpinBox.setMinimum(0)
        self.fontSizeSpinBox.setMaximum(72)

        self.fontColorComboBox = QComboBox(self)

        #layout of menu
        self.layout = QFormLayout()
        self.layout.addRow(self.tr("Font Family:"), self.fontFamilyComboBox)
        self.layout.addRow(self.tr("Font Size:"), self.fontSizeSpinBox)
        self.layout.addRow(self.tr("Font Color:"), self.fontColorComboBox)
        self.setLayout(self.layout)

class UICustomizeManager:
    def __init__(self, window) -> None:
        self.window = window

    def openMenu(self):
        menu = UICustomizeMenu(self, self.window)
        return menu


