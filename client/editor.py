
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from diff_match_patch import diff_match_patch
import logging
import msgpack
import sys
from random import randint

class Editor(QPlainTextEdit):
    upd_text = Signal(str)
    change_evt = Signal(str)
#hello world
    def __init__(self, socket):
        super(Editor, self).__init__()
        self.socket = socket
        self.setFrameStyle(QFrame.NoFrame)

        self.resize(1000, 500)

        self.text = ""

        self.upd_text.connect(self.update_text)

        self.gettext()
    
    def setTCPSocket(self, socket):
        self.socket = socket
    
    def gettext(self):
        bin = msgpack.packb({"text": True}, use_bin_type=True)
        self.socket.write(bin)
    
    def keyPressEvent(self, e):
        QPlainTextEdit.keyPressEvent(self, e)

        updated_text = self.toPlainText()

        patches = dmp.patch_make(self.text, updated_text)
        diff = dmp.patch_toText(patches)

        self.text = updated_text

        self.change_evt.emit(diff)
    
    @Slot(str)
    def update_text(self, patch):
        if "patch" in patch:
            diff = patch["patch"]
            patches = dmp.patch_fromText(diff)
            self.text, _ = dmp.patch_apply(patches, self.text)
        cursor = self.textCursor()
        old_pos = cursor.position()
        self.setPlainText(self.text)
        cursor.setPosition(old_pos)
        self.setTextCursor(cursor)