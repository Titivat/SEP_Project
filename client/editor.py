from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from diff_match_patch import diff_match_patch
import logging
import msgpack
import sys
from random import randint

logging.basicConfig(level=logging.INFO)

dmp = diff_match_patch()

class Main(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.socket = QTcpSocket(self)
        self.socket.waitForConnected(1000)
        self.socket.readyRead.connect(self.on_read)
        self.socket.error.connect(self.on_error)
        self.connect("127.0.0.1", 5000)

        self.setGeometry(400, 400, 800, 600)

        self.unpacker = msgpack.Unpacker()

        self.editor = Editor(self.socket)
        self.editor.change_evt.connect(self.on_change)

        self.setCentralWidget(self.editor)
    
    def connect(self, host, port):
        self.socket.connectToHost(host, port, QIODevice.ReadWrite)
    
    def on_read(self):
        instr = QDataStream(self.socket)
        instr.setVersion(QDataStream.Qt_5_0)
        buf = instr.readRawData(1024**2)
        if not buf:
            return
        self.unpacker.feed(buf)
        for data in self.unpacker:
            logging.info(f"[SERVER] {data}")
            self.editor.update_text(data)

    def on_error(self, socketError):
        logging.error(socketError)
    
    def on_change(self, diff):
        bin = msgpack.packb({"patch": diff}, use_bin_type=True)
        self.socket.write(bin)

class Editor(QPlainTextEdit):
    upd_text = Signal(str)
    change_evt = Signal(str)

    def __init__(self, socket):
        super(Editor, self).__init__()
        self.socket = socket
        self.setFrameStyle(QFrame.NoFrame)

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

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
