
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
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
