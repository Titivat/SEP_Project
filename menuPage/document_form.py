import sys
import PySide2.QtWidgets as QtWidgets
from PySide2.QtWidgets import QListWidget, QDialog, QApplication, QVBoxLayout , QPushButton
from PySide2.QtCore import *
import PySide2.QtGui
from client import Message_dialog
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

        self.widgetText = QtWidgets.QLabel( "document name" )
        open_document_button = QtWidgets.QPushButton("Open document")
        delete_document_button = QtWidgets.QPushButton("Delete document")
        show_document_id_button = QtWidgets.QPushButton("Show document ID")

        widgetLayout = QtWidgets.QHBoxLayout()

        widgetLayout.addWidget( self.widgetText )
        widgetLayout.addWidget( open_document_button )
        widgetLayout.addWidget( delete_document_button )
        widgetLayout.addWidget( show_document_id_button )
        widgetLayout.addStretch()

        open_document_button.clicked.connect( self.openDocument )
        delete_document_button.clicked.connect( self.delete_document_button )
        show_document_id_button.clicked.connect( self.show_text_id )

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

    def show_text_id( self ):
        mesage_dialog = Message_dialog.Message_dialog( self )
        mesage_dialog.set_editor_id( self.document_id )
        mesage_dialog.show()

    def openDocument( self ):
        self.socket.write(msgpack.packb({"action":"open","id": self.document_id })) 

    def delete_document_button( self ):

        self.parent.ui.listWidget.takeItem( self.parent.ui.listWidget.row( self.itemN ) )

        if self.is_share_documnet == True:
            self.socket.write(msgpack.packb({"action":"remove","id": self.document_id })) 
            return
            
        self.socket.write(msgpack.packb({"action":"delete","id": self.document_id })) 