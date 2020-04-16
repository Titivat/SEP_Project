import sys
import random
import time
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import time
from threading import Thread
from MessageThread import MessageThread
    
class ClientUi(QWidget):
    
    def __init__(self):       
        QWidget.__init__(self, None)
        self.resize( 1000, 500 )
        vbox = QVBoxLayout()
        self.textEdit1 = QTextEdit( self )
        vbox.addWidget( self.textEdit1 )

        #self.textEdit1.textChanged.connect( self.reciveData )
        #self.connect( self.receive_thread , SIGNAL('MESSAGE'))
        
        self.setLayout(vbox)
        #self.show()
        
    def sendData( self ):

        if self.recive == True:
            print('not sending the same message')
            self.recive = False
        else:
            texteditMessage = self.textEdit1.toPlainText()
            print(f'{ self.id :<{self.HEADER}}')

            try:
                message = f'{ self.id :<{self.HEADER}}' + texteditMessage[-1]
            except:
                pass

            self.socket_push.send_string( message )

    def reciveData(self):
        
        while True:
            message = self.socket_sub.recv_string()
            print('message')
            if not message:
                print('recive empty string')
            elif self.id == message[:self.HEADER].strip():
                 print('recive send message')
            else:
                self.textEdit1.append( message[self.HEADER:] )
                self.recive = True

""" if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Simple_timer_window()
    sys.exit(app.exec_())
 """