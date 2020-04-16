from ServerConnector import ServerConnector
from PySide2.QtCore import  *

class MessageThread( QThread ):
    over = Signal( bytes )

    def __init__( self , parent = None ):
        super( MessageThread , self ).__init__( parent )
        self.network = None

    def setNetWork( self , network ):
        self.network= network

    def run(self):
        while True:
            message = self.network.getMessage()
            print( message )
            self.over.emit( message )
