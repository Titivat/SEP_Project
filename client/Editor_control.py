from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from PySide2.QtGui import *
from diff_match_patch import diff_match_patch
from .Editor_view import Editor_view
import logging
import msgpack
import sys
import os 
from random import randint

logging.basicConfig(level=logging.INFO)

class Editor_control(QWidget):
    def __init__( self , socket ):
        super( Editor_control , self).__init__()
        self.socket = socket

        self._message_box =  QMessageBox()

        self.unpacker = msgpack.Unpacker()
        #self.socket = socket

        self.setGeometry(400, 400, 800, 400)

        self.unpacker = msgpack.Unpacker()

        self.editor = Editor_view( self ,self.socket )
        self.editor.editor.change_evt.connect( self.on_change )

        layout = QVBoxLayout()
        layout.addWidget( self.editor )

        self.setLayout(layout)

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
            self.editor.editor.update_text(data)

    def on_error(self, socketError):
        logging.error(socketError)
    
    def on_change(self, diff):
        bin = msgpack.packb({"action":"edit", "patch": diff}, use_bin_type=True)
        self.socket.write(bin)

def main():
    app = QApplication(sys.argv)

    main = Editor_control()

    main.show()
    sys.exit(app.exec_())

#if __name__ == '__main__':
#    main()
