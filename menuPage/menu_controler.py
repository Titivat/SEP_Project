from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtNetwork import *
from .menu_view import Ui_Form
from .document_form import Document_Form
import msgpack
import random
import sys
import time 

class Menu_controler( QWidget ):
    def __init__( self , socket ):
        QWidget.__init__(self, None)
        self.socket = socket 

        self.on_share_drive = False

        self.unpacker = msgpack.Unpacker()
        self.ui = Ui_Form()
        self.ui.setupUi( self )

        self.ui.adddocbutton.clicked.connect( self.add_document )
        self.ui.mydrivebutton.clicked.connect( self.my_drive )
        self.ui.sharedrivebutton.clicked.connect( self.share_drive )
        self.ui.logoutbutton.clicked.connect( self.log_out )

    def my_drive( self ):
        if self.on_share_drive:
            self.load_my_document()
            self.on_share_drive = False

            self.set_page_status( "My Drive" )

    def share_drive( self ):
        if not self.on_share_drive:
            self.load_share_document()

            self.set_page_status( "Share Drive" )

            self.on_share_drive = True
    
    def set_page_status( self, text ):
        _translate = QCoreApplication.translate

        self.ui.pagestatus.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; font-weight:600;\"> " + text + "</span></p></body></html>"))

    def add_document( self ): 
        document_name, add = QInputDialog.getText(self, 'add', 'Enter Document name')

        if not add:
            pass
        elif self.on_share_drive == False:
            self.socket.write( msgpack.packb({"action":"create", "name": document_name  })) 

        elif self.on_share_drive == True:
            self.socket.write( msgpack.packb({"action":"add", "id": document_name  })) 
            
    def add_list_view( self , name , id ):
        new_dociment = Document_Form(  self  , self.socket , self.on_share_drive )
        new_dociment.set_document_name( name )
        new_dociment.set_document_id( id )

        self.ui.listWidget.addItem( new_dociment.getItemN() )
        self.ui.listWidget.setItemWidget( new_dociment.getItemN() , new_dociment.getWidget() )

    def log_out( self ):
        self.socket.write(msgpack.packb({"action":"logout" })) 
        self.close()
    
    def load_my_document( self ):
        self.ui.listWidget.clear() 
        self.socket.write(msgpack.packb({"action":"documents"}))

    def load_share_document( self ):
        self.ui.listWidget.clear() 
        self.socket.write(msgpack.packb({"action":"shareddocuments"}))
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    clinet = Menu_controler()

    sys.exit(app.exec_())

    
