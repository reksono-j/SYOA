BUTTON_STYLE = """
QPushButton {
    background-color: #6eb1ff; 
    color: darkblue; 
    border: 2px solid transparent; 
    border-radius: 5px; 
}
QPushButton:hover {
    background-color: #00bbff; 
    color: white;
    border: 2px solid #0056b3; 
}
QPushButton:pressed {
    background-color: #004f99; 
    color: white;
    border: 2px solid #003d80; 
}
"""
PROJECTMENU_STYLE = """
QMainWindow {
    background-color: #f0f0f0;
}
QPushButton {
    background-color: #007BFF;
    border-radius: 5px;
    padding: 10px;
}
QPushButton:hover {
    background-color: #0056b3;
}
QListWidget {
    background-color: white;
    border: 1px solid #007BFF;
    border-radius: 5px;
}
QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #e0e0e0;
}
QListWidget::item:selected {
    background-color: #007BFF;
    color: white;
}
QTextEdit {
    background-color: white;
    border: 1px solid #007BFF;
    border-radius: 5px;
}
"""


MENUBAR_STYLE = """
QMenuBar {
    background-color: #039dfc;
    spacing: 0px;
    margin: 0px;
}
QMenuBar::item {
    padding: 10px; 
}
QMenuBar::item:selected {
    background-color: #A0A0A0; 
    color: white;
    border: 2px solid #007BFF;
    border-radius: 5px;
}
QMenu { 
    background-color: #039dfc; 
}
QMenu::item { 
    padding: 10px 15px;
    margin: 0;
    border-bottom: 1px solid #A0D3FF;
}
QMenu::item:selected {
    background-color: #0077cc;
}
QMenu::item:last { 
    border-bottom: none;
}
"""

STATUSBAR_STYLE = """
QStatusBar {
    background-color: #039dfc;
}
"""

TABBAR_STYLE = """
QTabBar {
    background: #ffffff; 
    border: none;
}
QTabBar::tab:first-child {
    background: #e0e0e0;
    padding: 10px 15px;
    border: none;
    margin: 0px; 
    border-bottom: none; 
}
QTabBar::tab:last-child {
    background: #e0e0e0;
    padding: 10px 15px;
    border: none; 
    margin: 0px; 
    border-bottom: none;
}
QTabBar::tab {
    background: #e0e0e0;
    padding: 10px 15px; 
    border: 1px solid transparent;
    border-bottom: none;
    margin: 0px; 
}
QTabBar::tab:!first-child:!last-child {
    border-left: 2px solid #ccc; 
    border-right: 2px solid #ccc; 
}
QTabBar::tab:selected {
    background: #007acc; 
    color: #ffffff; 
    font-weight: bold; 
}
QTabBar::tab:hover {
    background: #d0d0d0; 
}
QStackedWidget {
    border: 1px solid #ccc; 
    background: #ffffff; 
    padding: 10px;
    margin-top: -1px; 
}
QPushButton {
    background-color: #007acc; 
    color: #ffffff; 
    border: none; 
    border-radius: 5px; 
    padding: 10px 15px; 
}
QPushButton:hover {
    background-color: #005f99; 
}
"""


APP_STYLE = """
    * {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13pt;
    }

    QWidget {
        background-color: #1A1E24; 
        color: #E5E9F0;
    }
    
    /* Menu */
    QMenu {
        background-color: #2E3440; 
        color: #E5E9F0; 
        border: 1px solid #4C566A; 
    }
    QMenu::item {
        background-color: transparent;
        padding: 8px 12px;
    }
    QMenu::item:selected {
        background-color: #4C566A; 
    }
    
    /* Menu Bar */
    QMenuBar {
        background-color: #2E3440; 
        color: #E5E9F0;
        padding: 5px;
    }
    QMenuBar::item {
        background-color: #2E3440; 
        padding: 8px 12px;
    }
    QMenuBar::item:selected {
        background-color: #4C566A;
    }

    /* Status Bar */
    QStatusBar {
        background-color: #2E3440;
        color: #E5E9F0;
        padding: 5px;
    }

    /* Tab Bar */
    QTabWidget {
        background-color: #2E3440;
        border: none;
    }
    QTabBar {
        background-color: #2E3440; 
        color: #E5E9F0;
        font-weight: bold;
    }
    QTabBar::tab {
        background-color: #4C566A; 
        color: #E5E9F0;
        padding: 10px;
        border: 2px solid transparent; 
        border-radius: 6px;
    }
    QTabBar::tab:selected {
        background-color: #5E81AC;
        border: 2px solid #88C0D0;
    }
    QTabBar::tab:hover {
        background-color: #4C566A; 
    }

    /* Stacked Widget */
    QStackedWidget {
        padding: 0px; 
        margin: 0px;  
    }

    /* List Widget */
    QListWidget {
        background-color: #2E3440; 
        border: 2px solid #4C566A; 
        border-radius: 6px;
    }
    QListWidget::item {
        background-color: #4C566A; 
        color: #E5E9F0;
        padding: 8px;
        margin: 0 0 2px 0;
    }
    QListWidget::item:selected {
        background-color: #88C0D0; 
        color: #1A1E24;
    }
    QListWidget::item:hover {
        background-color: #5E81AC;
        color: #1A1E24;
    }

    /* Buttons */
    QPushButton {
        background-color: #4C566A;
        color: #ECEFF4;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #5E81AC;
    }
    QPushButton:pressed {
        background-color: #3B4252;
    }

    /* Labels */
    QLabel {
        color: #E5E9F0;
        font-weight: 500;
    }

    QLineEdit, QTextEdit {
        background-color: #2E3440;
        color: #ECEFF4;
    }

    /* ComboBox and Drop-downs */
    QComboBox {
        background-color: #2E3440;
        color: #ECEFF4;
        padding: 6px 10px;
        border: 2px solid #4C566A;
        border-radius: 6px;
    }
    QComboBox::drop-down {
        background-color: #3B4252;
        border-left: 1px solid #4C566A;
    }

    /* Sliders */
    QSlider::groove:horizontal {
        height: 8px;
        background-color: #434C5E;
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        width: 20px;
        height: 20px;
        background-color: #88C0D0;
        border-radius: 10px;
        margin: -6px 0;
    }

    /* Progress Bar */
    QProgressBar {
        text-align: center;
        color: #ECEFF4;
        background-color: #3B4252;
        border: 2px solid #4C566A;
        border-radius: 8px;
        padding: 4px;
    }
    QProgressBar::chunk {
        background-color: #5E81AC;
        border-radius: 6px;
    }

    /* Scrollbars */
    QScrollBar:vertical, QScrollBar:horizontal {
        background-color: #3B4252;
        width: 14px;
    }
    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
        background-color: #88C0D0;
        border-radius: 7px;
        min-height: 30px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        background: none;
    }
    
    /* Home Menu Frame */
    #homeMenuFrame {
        background-color: #2E3440;
        border: 1px solid #4C566A; 
        border-radius: 6px;          
        padding: 10px;               
    }

    #homeMenuFrame QPushButton {
        background-color: #4C566A;  
        color: #ECEFF4;             
        padding: 12px 20px;         
        border-radius: 6px;         
        font-weight: bold;         
    }
    
    #homeMenuFrame QPushButton:hover {
        background-color: #5E81AC;  
    }

    #homeMenuFrame QPushButton:pressed {
        background-color: #3B4252; 
    }

    #homeMenuFrame QVBoxLayout {
        margin: 0;                  
        spacing: 5;             
    }
    
    /* Project Menu */
    #projectMenuTabBar QTabBar {
        background-color: #3B4252; 
        color: #E5E9F0;
        font-weight: bold;
    }

    #projectMenuTabBar QTabBar::tab {
        background-color: #4C566A; 
        color: #E5E9F0;
        padding: 10px;
        border: 2px solid transparent; 
        border-radius: 6px;
    }

    #projectMenuTabBar QTabBar::tab:selected {
        background-color: #5E81AC;
        border: 2px solid #88C0D0;
    }

    #projectMenuTabBar QTabBar::tab:hover {
        background-color: #4C566A; 
    }

    #projectMenuStack QPushButton {
        background-color: #4C566A;  
        color: #ECEFF4;            
        padding: 12px 20px;          
        border-radius: 6px;         
        font-weight: bold;         
    }

    #projectMenuStack QPushButton:hover {
        background-color: #5E81AC;   
    }

    #projectMenuStack QPushButton:pressed {
        background-color: #3B4252;
    }
"""
