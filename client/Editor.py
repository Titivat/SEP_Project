from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtPrintSupport import *
from .LineNumberArea import LineNumberArea
from diff_match_patch import diff_match_patch
import logging
import msgpack
import sys
from random import randint

dmp = diff_match_patch()

class Editor(QPlainTextEdit):
    upd_text = Signal(str)
    change_evt = Signal(str)
    
    def __init__(self, socket):
        super(Editor, self).__init__()
        self.socket = socket
        self.setFrameStyle(QFrame.NoFrame)

        self.resize(1000, 500)

        self.text = ""

        self.upd_text.connect( self.update_text )

        self.lineNumberArea = LineNumberArea(self)

        self.connect(self, SIGNAL('blockCountChanged(int)'), self.updateLineNumberAreaWidth)
        self.connect(self, SIGNAL('updateRequest(QRect,int)'), self.updateLineNumberArea)

        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


    def updateLineNumberArea(self, rect, dy):

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)


    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth(), cr.height()))


    def lineNumberAreaPaintEvent(self, event):
        mypainter = QPainter(self.lineNumberArea)

        mypainter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(Qt.black)
                mypainter.drawText(0, top, self.lineNumberArea.width(), height,
                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
        
    def keyPressEvent(self, e):
        QPlainTextEdit.keyPressEvent(self, e)

        updated_text = self.toPlainText()

        patches = dmp.patch_make(self.text, updated_text)
        diff = dmp.patch_toText(patches)

        self.text = updated_text

        self.change_evt.emit(diff)
    
    @Slot(str)
    def update_text(self, patch):
        if "text" in patch and patch["text"]:
            self.text = patch["text"]
        elif "patch" in patch:
            diff = patch["patch"]
            patches = dmp.patch_fromText(diff)
            self.text, _ = dmp.patch_apply(patches, self.text)
        else:
            self.text = ""
        cursor = self.textCursor()
        old_pos = cursor.position()
        self.setPlainText(self.text)
        cursor.setPosition(old_pos)
        self.setTextCursor(cursor)
