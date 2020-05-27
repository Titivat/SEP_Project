from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from PySide2.QtGui import *
from diff_match_patch import diff_match_patch
from Editor import Editor
import logging
import msgpack
import sys
from random import randint

logging.basicConfig(level=logging.INFO)

dmp = diff_match_patch()

class Editor_control(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.socket = QTcpSocket(self)
        self.socket.waitForConnected(1000)
        self.socket.readyRead.connect(self.on_read)
        self.socket.error.connect(self.on_error)
        self.connect("127.0.0.1", 5000)

        self.setGeometry(400, 400, 800, 400)

        self.unpacker = msgpack.Unpacker()

        self.editor = Editor(self.socket)
        self.editor.change_evt.connect(self.on_change)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        #file_menu = self.menuBar().addMenu("&File")

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

def main():
    app = QApplication(sys.argv)

    main = Editor_control()

    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
