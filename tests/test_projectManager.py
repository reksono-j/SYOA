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
import shutil
import json

from src_alt.editor.projectManager import ProjectManager

class Test(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_projects"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.manager = ProjectManager(baseDirectory=self.test_dir)
        
        self.project_name = "projectManagerTest"
        workingDir = os.path.dirname(os.path.abspath(__file__))
        self.parent_path = os.path.dirname(workingDir)

        return super().setUp()
    
    def tearDown(self):
        if os.path.exists(os.path.join(self.parent_path, "projectManagerTest")):
            shutil.rmtree(os.path.join(self.parent_path, "projectManagerTest"))

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_create_project(self):
        metadata = self.manager.createProject(self.project_name)
        self.assertIn("id", metadata)
        self.assertIn("createdAt", metadata)
        self.assertEqual(metadata["name"], self.project_name)

        

    def test_create_project_invalid_name(self):
        with self.assertRaises(ValueError):
            self.manager.createProject("Invalid Project Name!")

    def test_create_project_already_exists(self):
        self.manager.createProject(self.project_name)
        with self.assertRaises(FileExistsError):
            self.manager.createProject(self.project_name)

    def test_is_valid_project_name(self):
        self.assertTrue(self.manager.isValidProjectName("Valid_Project123"))
        self.assertFalse(self.manager.isValidProjectName("Invalid Project!"))

    def test_list_projects(self):
        if os.path.exists(os.path.join(self.parent_path, "someProject1")):
            shutil.rmtree(os.path.join(self.parent_path, "someProject1"))
        if os.path.exists(os.path.join(self.parent_path, "someProject2")):
            shutil.rmtree(os.path.join(self.parent_path, "someProject2"))

        project_names = ["someProject1", "someProject2"]
        for name in project_names:
            self.manager.createProject(name)
        listed_projects = self.manager.listProjects()
        self.assertListEqual(listed_projects, listed_projects)

        if os.path.exists(os.path.join(self.parent_path, "someProject1")):
            shutil.rmtree(os.path.join(self.parent_path, "someProject1"))
        if os.path.exists(os.path.join(self.parent_path, "someProject2")):
            shutil.rmtree(os.path.join(self.parent_path, "someProject2"))

    def test_load_project(self):
        created_metadata = self.manager.createProject(self.project_name)
        loaded_metadata = self.manager.loadProject(self.project_name)
        self.assertEqual(created_metadata, loaded_metadata)

    def test_load_project_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            self.manager.loadProject("NonExistentProject")

    def test_set_start_scene(self):
        self.manager.createProject(self.project_name)
        self.manager.setStartScene("StartScene")
        loaded_metadata = self.manager.loadProject(self.project_name)
        self.assertEqual(loaded_metadata.get("startScene"), "StartScene")