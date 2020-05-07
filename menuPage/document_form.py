import sys
import PySide2.QtWidgets as QtWidgets
from PySide2.QtWidgets import QListWidget, QDialog, QApplication, QVBoxLayout , QPushButton
import PySide2.QtCore
import PySide2.QtGui

class Document_Form(QDialog):
    def __init__( self , parent = None):
        super( Document_Form , self).__init__( parent )
        self.itemN = QtWidgets.QListWidgetItem()

        self.widget = QtWidgets.QWidget()
        self.widgetText = QtWidgets.QLabel( "document_name" )
        widgetButton = QtWidgets.QPushButton("open ducument")
        widgetLayout = QtWidgets.QHBoxLayout()
        widgetLayout.addWidget( self.widgetText )
        widgetLayout.addWidget(widgetButton)
        widgetLayout.addStretch()

        widgetButton.clicked.connect( self.openDocument )

        widgetLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.widget.setLayout(widgetLayout)
        self.itemN.setSizeHint( self.widget.sizeHint() )

    def getItemN( self ):
        return self.itemN
        
    def getWidget( self ):
        return self.widget

    def set_document_name( self , name ):
        self.widgetText.setText( name )

    def openDocument( self ):
        pass