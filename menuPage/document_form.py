import sys
import PySide2.QtWidgets as QtWidgets
from PySide2.QtWidgets import QListWidget, QDialog, QApplication, QVBoxLayout , QPushButton
from PySide2.QtCore import *
import PySide2.QtGui
import msgpack

class Document_Form(QDialog):
    def __init__( self , parent = None , socket = None , is_share_documnet = None):
        super( Document_Form , self).__init__( parent )
        self.is_share_documnet = is_share_documnet

        self.parent = parent

        self.socket = socket

        self.document_id = None

        self.itemN = QtWidgets.QListWidgetItem()

        self.widget = QtWidgets.QWidget()

        self.widgetText = QtWidgets.QLabel( "docmunet name" )

        open_document_button = QtWidgets.QPushButton("Open ducument")

        delete_document_button = QtWidgets.QPushButton("Delete ducument")

        widgetLayout = QtWidgets.QHBoxLayout()

        widgetLayout.addWidget( self.widgetText )
        widgetLayout.addWidget( open_document_button )
        widgetLayout.addWidget( delete_document_button )
        widgetLayout.addStretch()

        open_document_button.clicked.connect( self.openDocument )
        delete_document_button.clicked.connect( self.delete_document_button )

        widgetLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.widget.setLayout(widgetLayout)
        self.itemN.setSizeHint( self.widget.sizeHint() )

    def get_my_id( self ):
        return self.my_id

    def get_document_id( self ):
        return self.document_id 

    def set_document_id( self , id ):
        self.document_id  = id 
    
    def getItemN( self ):
        return self.itemN
        
    def getWidget( self ):
        return self.widget

    def set_document_name( self , name ):
        self.widgetText.setText( name )

    def openDocument( self ):
        print( self.document_id )
        self.socket.write(msgpack.packb({"action":"open","id": self.document_id })) 

    def delete_document_button( self ):

        self.parent.ui.listWidget.takeItem( self.parent.ui.listWidget.row( self.itemN ) )

        if self.is_share_documnet == True:
            self.socket.write(msgpack.packb({"action":"remove","id": self.document_id })) 
            return
            
        self.socket.write(msgpack.packb({"action":"delete","id": self.document_id })) 