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

        self.sendPackage = Package( self.id )
        self.recivePackage = Package()
       
        self.serverConnector = ServerConnector()

        self.ui = ClientUi()

        self.receive_thread = MessageThread( )
        self.receive_thread.setNetWork( self.serverConnector )
        self.receive_thread.over.connect(self.updateTextEditor )
        self.receive_thread.start()
        #self.connect( self.receive_thread, SIGNAL('MESSAGE') )

        self.ui.show( )

    @Slot( str )
    def updateTextEditor( self , message ):
        self.ui.textEdit1.append( message )

if __name__ == '__main__':
    app = QApplication(sys.argv)

    clinet = ClientControler()

    sys.exit(app.exec_())

    