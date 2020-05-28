from loginPage import login_controler
from menuPage import menu_controler, document_form
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtNetwork import *
import msgpack
import sys

class Application( QMainWindow ):

    def __init__( self ):
        QMainWindow.__init__(self, None)

        self.socket = QTcpSocket(self)
        self.socket.waitForConnected(1000)
        self.socket.readyRead.connect(self.on_read)
        self.socket.error.connect(self.on_error)
        self.connect("127.0.0.1", 5000)

        self._message_box = QMessageBox()

        self.unpacker = msgpack.Unpacker()

        self.menu_page = menu_controler.Menu_controler( self.socket )

        self.login_page = login_controler.Login_controler( self.socket )
        self.login_page.show()
 
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
            print( (f"[SERVER] {data}") )
            if data["ctx"] == "register":
                if data["success"]:
                    self._message_box.setText(str('register success' ))
                    self._message_box.show()
                else :
                    self._message_box.setText(str('fail register ' + data["err"] ))
                    self._message_box.show()

            if data["ctx"] == "login":
                if data["success"]:
                    self.login_page.close()
                    self.menu_page.load_my_document()
                    self.menu_page.show()
                else:
                    self._message_box.setText(str('fail login ' +  data["err"] ))
                    self._message_box.show()

            if data["ctx"] == "create":
                print("create sucessfull1")
                if data["success"]:
                    self.menu_page.add_list_view( data["name"], data["id"] )

            if data["ctx"] == "documents":
                print("hello")
                for document in data["documents"]:
                    self.menu_page.add_list_view( document["name"], document["id"] )

            if data["ctx"] == "shareddocuments":
                for document in data["documents"]:
                    self.menu_page.add_list_view( document["name"], document["id"] )

    def on_error(self, socketError):
        print( socketError )

if __name__ == '__main__':
    app = QApplication(sys.argv)

    application = Application()

    sys.exit(app.exec_())

    

