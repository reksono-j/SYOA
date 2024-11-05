import sys
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QWidget, QMessageBox, QTextEdit
from PySide6.QtGui import QPainter, QColor, QFont, QTextFormat
from PySide6.QtCore import Qt

# TODO: Connect all of the color options to the preferences

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.resizing = False
        self.minWidth = 40 # TODO: Add an option in the settings to save this

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if abs(event.pos().x() - self.width()) < 5:
                self.resizing = True

    def mouseMoveEvent(self, event):
        if self.resizing:
            newWidth = event.x()  # Get mouse horizontal position
            if newWidth < self.minWidth:
                newWidth = self.minWidth

            self.setFixedWidth(newWidth)
            self.editor.setViewportMargins(self.width(), 0, 0, 0)
            self.editor.updateLineNumbers()

    def mouseReleaseEvent(self, event):
        self.resizing = False

class NumberedTextEdit(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)
        self.lineNumberArea.setFixedWidth(self.lineNumberArea.minWidth)
        
        self.verticalScrollBar().valueChanged.connect(self.updateLineNumbers)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.highlightCurrentLine()
        
        self.fontSize = self.font().pointSize()
        self.setFont(self.font())
        self.updateLineNumbers()

    def lineNumberAreaWidth(self):
        return self.lineNumberArea.width()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.lineNumberArea.setGeometry(0, 0, self.lineNumberArea.width(), self.height())
        self.setViewportMargins(self.lineNumberArea.width(), 0, 0, 0)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(50, 50, 50))  # Background color for line numbers
        painter.setPen(QColor(255, 255, 255))
        lineCount = self.blockCount()
        lineHeight = self.fontMetrics().height()
        fontMetrics = painter.fontMetrics()

        numberAreaWidth = self.lineNumberArea.width() / 2
        currentLine = self.textCursor().blockNumber()
        for i in range(lineCount):
            line = self.document().findBlockByNumber(i)
            if line.isVisible():
                lineY = int(self.blockBoundingGeometry(line).translated(self.contentOffset()).top())
                lineNumber = str(i + 1)
                numX = int(numberAreaWidth - fontMetrics.horizontalAdvance(lineNumber) / 2)
                if (i == currentLine):
                    # I'm writing it this way to avoid setting the pen on every line
                    painter.setPen(QColor(0, 120, 250)) 
                    painter.drawText(numX, lineY, self.lineNumberArea.width(), lineHeight, Qt.AlignLeft | Qt.AlignVCenter, lineNumber)
                    painter.setPen(QColor(255, 255, 255))
                else:
                    painter.drawText(numX, lineY, self.lineNumberArea.width(), lineHeight, Qt.AlignLeft | Qt.AlignVCenter, lineNumber)

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly(): # All non selected lines become readOnly
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(0, 120, 250, 40)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection() 
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
        self.updateLineNumbers()
        
    def updateLineNumbers(self):
        self.lineNumberArea.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.clearFocus()
        else:
            super().keyPressEvent(event)
        self.updateLineNumbers()  # Update line numbers when typing

    def changeFontSize(self, newSize):
        self.fontSize = newSize
        self.setFont(self.font())
        self.updateLineNumbers()

    def jumpToLine(self, line_number):
        if line_number < 1 or line_number > self.blockCount():
            QMessageBox.warning(self, "Invalid Line Number", "Please enter a valid line number.")
            return
        block = self.document().findBlockByNumber(line_number - 1)
        cursor = self.textCursor()
        cursor.setPosition(block.position())
        self.setTextCursor(cursor)
        self.ensureCursorVisible()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    textbox = NumberedTextEdit()
    textbox.resize(1000, 500)
    textbox.show()
    sys.exit(app.exec_())
