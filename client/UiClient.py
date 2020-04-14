import sys
import random
import time
import zmq
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import time

class Simple_timer_window(QWidget):
    
    def __init__(self):
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

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start( 10000 )

        self.setLayout(vbox)
        self.show()
        
    def updatePoision( self ):
        message = self.textEdit1.toPlainText()
        self.socket_push.send_string( message )
        
    def update(self):
        
        message = self.socket_sub.recv_string()
        print('Clinet Received:', message)
        
        if not message:
            print('I recive a empty')
        else:
            self.textEdit1.append( message )
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Simple_timer_window()

    sys.exit(app.exec_())
