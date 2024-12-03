from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabBar, QStackedWidget

class TabsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0) 
        
        # TabBar for the tabs
        self.tabBar = QTabBar()
        self.tabBar.setObjectName("projectMenuTabBar")
        self.tabBar.setFocusPolicy(Qt.StrongFocus)
        self.tabBar.setMovable(True)
        self.tabBar.currentChanged.connect(self.onTabChanged)
        
        # TabContents for the actual widgets
        self.tabContents = QStackedWidget()
        self.tabContents.setObjectName("projectMenuStack")
        self.tabContents.setContentsMargins(0, 0, 0, 0)  
        
        self.focusedIndex = 0  
        self.layout.addWidget(self.tabBar)
        self.layout.addWidget(self.tabContents)

    def addTab(self, title, contentWidget):
        self.tabBar.addTab(title)
        
        contentWidget.setContentsMargins(0, 0, 0, 0) 
        
        self.tabContents.addWidget(contentWidget)
        
        if self.tabBar.count() == 1:
            self.tabBar.setCurrentIndex(0)
            self.focusedIndex = 0

    def getAllTabs(self):
        tabs = []
        for index in range(self.tabBar.count()):
            tabTitle = self.tabBar.tabText(index)
            tabWidget = self.tabContents.widget(index)
            tabs.append((tabTitle, tabWidget))
        return tabs
    
    def getTabWidget(self, index):
        return self.tabContents.widget(index) if index < self.tabContents.count() else None
    
    def onTabChanged(self, index):
        self.tabContents.setCurrentIndex(index)
    
    
    def getTabIndex(self, title):
        tabs = self.getAllTabs()
        index = 0
        for tab in tabs:
            if tab[0] == title:
                return index
            index += 1
        return None

    def mousePressEvent(self, event):
        clickedTab = self.tabBar.tabAt(event.position().toPoint())
        if clickedTab >= 0:
            self.tabContents.setCurrentIndex(clickedTab)
        super().mousePressEvent(event)
