import sys
import random
import time
import zmq
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import time
from threading import Thread
    
class Simple_timer_window(QWidget):
    
    def __init__(self):
        self.HEADER = 5

        self.id = str( random.randrange(0, 101) )
        print( 'Id = ', self.id )
        self.recive = False

        self.context = zmq.Context()
        self.socket_push = self.context.socket(zmq.PUSH)
        self.socket_sub = self.context.socket(zmq.SUB)
        self.socket_push.connect('tcp://127.0.0.1:5557')
        self.socket_sub.connect('tcp://127.0.0.1:5558')

        self.socket_sub.subscribe('')
        
        QWidget.__init__(self, None)
        self.resize( 1000, 500 )
        vbox = QVBoxLayout()
        self.textEdit1 = QTextEdit( self )
        vbox.addWidget( self.textEdit1 )

        self.textEdit1.textChanged.connect( self.updatePoision )

        self.receive_thread = Thread( target= self.update )
        self.receive_thread.start()
        
        self.setLayout(vbox)
        self.show()
        
    def updatePoision( self ):

        if self.recive == True:
            print('not sending the same message')
            self.recive = False
        else:
            texteditMessage = self.textEdit1.toPlainText()
            print(f'{ self.id :<{self.HEADER}}')
            message = f'{ self.id :<{self.HEADER}}' + texteditMessage[-1]

            self.socket_push.send_string( message )

    def update(self):
        
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

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Simple_timer_window()
    sys.exit(app.exec_())
