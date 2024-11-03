BUTTON_STYLE = """
QPushButton {
    background-color: #6eb1ff; /* Default color */
    color: darkblue; /* Text color */
    border: 2px solid transparent; /* Default border */
    border-radius: 5px; /* Rounded corners */
}
QPushButton:hover {
    background-color: #00bbff; /* Change to a vibrant color on hover */
    color: white; /* Change text color on hover */
    border: 2px solid #0056b3; /* Add a border on hover */
}
QPushButton:pressed {
    background-color: #004f99; /* Darker shade when pressed */
    color: white; /* Change text color when pressed */
    border: 2px solid #003d80; /* Add a darker border when pressed */
}
QPushButton:focus {
    outline: none; /* Remove default outline */
    background-color: #6eb1ff; /* Change background color when focused */
    border: 2px solid #FFA500; /* Change border color when focused */
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
    spacing: 0px; /* Space between menu items */
    margin: 0px; /* No margin around the menu bar */
}
QMenuBar::item {
    padding: 10px; /* Padding for menu items */
}
QMenuBar::item:selected {
    background-color: #A0A0A0; /* Highlight color */
    color: white; /* Text color when highlighted */
    font-weight: bold; /* Bold text */
    border: 2px solid #007BFF; /* Border for selected item */
    border-radius: 5px; /* Rounded corners for border */
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
    background: #ffffff; /* Tab background color */
    border: none; /* Remove border for the tab bar */
}
QTabBar::tab:first-child {
    background: #e0e0e0; /* First tab color */
    padding: 10px 15px; /* Padding around tab text */
    border: none; /* No border for the first tab */
    margin: 0px; /* No margin */
    border-bottom: none; /* Remove bottom border */
}
QTabBar::tab:last-child {
    background: #e0e0e0; /* Last tab color */
    padding: 10px 15px; /* Padding around tab text */
    border: none; /* No border for the last tab */
    margin: 0px; /* No margin */
    border-bottom: none; /* Remove bottom border */
}
QTabBar::tab {
    background: #e0e0e0; /* Default tab color */
    padding: 10px 15px; /* Padding around tab text */
    border: 1px solid transparent; /* Make borders transparent */
    border-bottom: none; /* Remove bottom border */
    margin: 0px; /* No margin */
}
QTabBar::tab:!first-child:!last-child {
    border-left: 2px solid #ccc; /* Left border for middle tabs */
    border-right: 2px solid #ccc; /* Right border for middle tabs */
}
QTabBar::tab:selected {
    background: #007acc; /* Selected tab color */
    color: #ffffff; /* Text color for selected tab */
    font-weight: bold; /* Bold text for selected tab */
}
QTabBar::tab:hover {
    background: #d0d0d0; /* Hover color */
}
QStackedWidget {
    border: 1px solid #ccc; /* Border for content area */
    background: #ffffff; /* Background for content */
    padding: 10px; /* Padding for content */
    margin-top: -1px; /* Remove gap by slightly overlapping with tab bar */
}
QPushButton {
    background-color: #007acc; /* Button background color */
    color: #ffffff; /* Button text color */
    border: none; /* No border */
    border-radius: 5px; /* Rounded corners for buttons */
    padding: 10px 15px; /* Padding for button */
    font-size: 14px; /* Font size for button */
}
QPushButton:hover {
    background-color: #005f99; /* Darker shade on hover */
}
"""