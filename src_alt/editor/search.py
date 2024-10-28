import sys 
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class SearchMenu(QWidget):
    def __init__(self, SearchMenu, parent):
        super(SearchMenu, self).__init__(parent)
        self.parent = parent
        self.SearchManager = SearchManager
        self.initParameters()
        self.initUI()

    def initParameters(self):
        #parameters something
        return 1

    def initUI(self):
        self.setTitle("Search Menu")

        # set up accessibility

        # typing box

        # group box with vertical alignment of three search types - 1. In file 2.Links (compile first?) 3. In other files that are linked

        # Pop up that is an overlay that takes focus and has a text box in middle

        # Removes pop up on focus lost?

        # Maybe as a QDialog?


class SearchManager:
    def __init__(self, window) -> None:
        self.window = window
        self.menu = SearchManager(self, window)