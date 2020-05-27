from .login_view import Ui_Form
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtNetwork import *
import msgpack
import random
import sys

class Login_controler( QWidget ):

    def __init__( self , socket ):
        super( Login_controler , self).__init__()
        self.socket = socket

        self._message_box = QMessageBox()
    
        self.ui = Ui_Form()
        self.ui.setupUi( self )

        self.ui.loginbutton.clicked.connect( self.change_stange_login_button )
        self.ui.registerbutton.clicked.connect( self.change_stage_register_button )

    def change_stage_register_button( self ):
        user_name = self.ui.useredit.text()
        user_password = self.ui.passwordedit.text()

        if self.ui.loginbutton.text() == "Register":
            self.login_request( user_name, user_password )
        else:
            self.register_request( user_name, user_password)

    def login_request( self, user_name, user_password):
        self.socket.write(msgpack.packb({"action":"login", "username": user_name , "password": user_password })) 
        print("Login")

    def register_request( self, user_name, user_password ):
        self.socket.write(msgpack.packb({"action":"register", "username": user_name , "password": user_password })) 

    def change_stange_login_button( self ):
        if self.ui.loginbutton.text() == "Register":
            self.register_stage()
        else:
            self.login_stage()
    
    def register_stage( self ):
        self.ui.registerbutton.setText("register")
        self.ui.loginbutton.setText("back")

        self.ui.logintext.setText( "Register" ) 
        self.ui.logintext.setStyleSheet(" color: #FFFFFF; font-size: 30px;font-weight: bold;")
        self.ui.logintext.setGeometry( QRect( 85, 10, 150, 41))
  
    def login_stage( self ):
      
        self.ui.registerbutton.setText("Login")
        self.ui.loginbutton.setText("Register")

        self.ui.logintext.setText( "Login" ) 
        self.ui.logintext.setStyleSheet(" color: #FFFFFF; font-size: 30px;font-weight: bold;")
        self.ui.logintext.setGeometry( QRect( 95, 10, 150, 41))

#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#
#    clinet = Login_controler()
#
#    sys.exit(app.exec_())

    