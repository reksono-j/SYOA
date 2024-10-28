from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabBar, QStackedWidget
from styles import TABBAR_STYLE

class TabsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0) 
        self.setStyleSheet(TABBAR_STYLE)
        
        # TabBar for the tabs
        self.tabBar = QTabBar()
        self.tabBar.setFocusPolicy(Qt.StrongFocus)
        self.tabBar.setMovable(True)
        
        # TabContents for the actual widgets
        self.tabContents = QStackedWidget()
        self.tabContents.setContentsMargins(0, 0, 0, 0)  # Ensure no margins here
        self.tabContents.setStyleSheet("padding: 0px; margin: 0px;")  # Set padding and margin to zero
        
        self.tabBar.installEventFilter(self)
        self.focusedIndex = 0  
        self.layout.addWidget(self.tabBar)
        self.layout.addWidget(self.tabContents)

    def addTab(self, title, contentWidget):
        self.tabBar.addTab(title)
        
        # Set the content widget's margins and padding
        contentWidget.setContentsMargins(0, 0, 0, 0)  # Ensure no margins on the widget
        contentWidget.setStyleSheet("padding: 0px; margin: 0px;")  # Set padding and margin to zero
        
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
    
    def eventFilter(self, obj, event):
        if obj == self.tabBar:
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Left or event.key() == Qt.Key_Right:
                    if event.key() == Qt.Key_Left:
                        newIndex = (self.focusedIndex - 1) % self.tabBar.count()
                    else:
                        newIndex = (self.focusedIndex + 1) % self.tabBar.count()
                    self.tabBar.setCurrentIndex(newIndex)
                    self.focusedIndex = newIndex
                elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                    self.tabContents.setCurrentIndex(self.focusedIndex)
            elif event.type() == QEvent.FocusOut:
                self.tabBar.setCurrentIndex(self.tabContents.currentIndex())
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        clickedTab = self.tabBar.tabAt(event.position().toPoint())
        if clickedTab >= 0:
            self.tabContents.setCurrentIndex(clickedTab)
        super().mousePressEvent(event)
