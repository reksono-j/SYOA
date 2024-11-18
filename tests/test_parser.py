import unittest
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QDialog, QLineEdit,
    QFormLayout, QLabel, QKeySequenceEdit,QWidget,QVBoxLayout, QComboBox,
    QAccessibleWidget, QGroupBox, QFontComboBox, QSpinBox, QTextEdit
)
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
import json
import copy
import os
from pathlib import Path
import sys
import json
import shutil

from src_alt.editor import parser

class Test(unittest.TestCase):
    def setUp(self):
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
    def test_buildScene(self):
        ExampleScript = """Speaker1 : Hello world
            CHOICE Hi there
            Speaker2: Hi there
            END
            Choice Pick up rock
            You picked up a rock
            modify rock add 1 
            END
            IF rock eq 1
            Speaker1 : That's a sweet rock
            Speaker2 : Isn't it?
            ELSE
            Speaker 1 looks at the ground, leans over, and picks up a rock.
            Speaker1 : Wow this is an awesome rock.
            Speaker2: Woah, you're right.
            END
            Branch Scene2"""
        
        scene = parser.readScript(ExampleScript)
        lines = scene.lines
        combined = ""
        
        correct = """
            Dialogue(Speaker1, Hello world)
            Choice([ChoiceOptions(Hi there, [Dialogue(Speaker2, Hi there)]), ChoiceOptions(Pick up rock, [Dialogue(, You picked up a rock), Modify(ADD, rock, 1)])])
            Conditional(EQ, rock, 1, [Dialogue(Speaker1, That's a sweet rock), Dialogue(Speaker2, Isn't it?)], [Dialogue(, Speaker 1 looks at the ground, leans over, and picks up a rock.), Dialogue(Speaker1, Wow this is an awesome rock.), Dialogue(Speaker2, Woah, you're right.)])
            Branch(Scene2)
        """
        self.assertEqual(correct,correct)