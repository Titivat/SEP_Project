from ClientUi import ClientUi
from MessageThread import MessageThread
from ServerConnector import ServerConnector
from Package import Package
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import random
import sys

class ClientControler( QMainWindow ):

    def __init__( self ):
        QMainWindow.__init__(self, None)

        self.id = str( random.randrange(0, 101) )
        self.recive = True

        self.sendPackage = Package( self.id )
       
        self.serverConnector = ServerConnector()

        self.ui = ClientUi()
        self.ui.textEdit.textChanged.connect( self.sendTextUpdate )

        self.receiveThread = MessageThread( )
        self.receiveThread.setNetWork( self.serverConnector )
        self.receiveThread.message.connect(self.updateTextEditor )
        self.receiveThread.start()

        self.ui.show( )

    def sendTextUpdate( self ):
        if self.recive == True:
            self.recive = False
        else:
            textEditMessage = self.ui.textEdit.toPlainText()
            self.sendPackage.setData( textEditMessage[-1] )
            self.serverConnector.sendData( self.sendPackage )

    @Slot( str )
    def updateTextEditor( self , message ):
        if message.getId() == self.id:
            print("do notthing")
        else:
            self.ui.textEdit.append( message.getData() )
            self.recive = True

if __name__ == '__main__':
    app = QApplication(sys.argv)

    clinet = ClientControler()

    sys.exit(app.exec_())

    