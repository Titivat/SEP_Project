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

        self.tcpSocket = QTcpSocket(self)
        self.makeRequest()
        self.tcpSocket.waitForConnected(1000)
        self.tcpSocket.readyRead.connect(self.dealCommunication)
        self.tcpSocket.error.connect(self.displayError)

        self.setGeometry(400, 400, 800, 600)

        self.unpacker = msgpack.Unpacker()

        self.editor = Editor(self.tcpSocket)

        self.setCentralWidget(self.editor)
    
    def makeRequest(self):
        HOST = '127.0.0.1'
        PORT = 5000
        self.tcpSocket.connectToHost(HOST, PORT, QIODevice.ReadWrite)
    
    def dealCommunication(self):
        instr = QDataStream(self.tcpSocket)
        instr.setVersion(QDataStream.Qt_5_0)
        buf = instr.readRawData(1024**2)
        if not buf:
            return
        self.unpacker.feed(buf)
        for data in self.unpacker:
            logging.info(f"[SERVER] {data}")
            self.editor.update_text(data)

    def displayError(self, socketError):
        logging.error(socketError)

class Editor(QPlainTextEdit):
    upd_text = Signal(str)

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

        bin = msgpack.packb({"patch": diff}, use_bin_type=True)
        self.socket.write(bin)
    
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
