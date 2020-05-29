from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from PySide2.QtGui import *
import pyperclip

class Message_dialog(QDialog):

    def __init__( self, parent=None ):
        super( Message_dialog , self).__init__(parent)
        self.setWindowTitle("Text id")

        self.editor_id = None

        self.id_lebale = QLabel( "id" )
        self.copy_button = QPushButton("Copy")
        
        layout = QVBoxLayout()
        layout.addWidget(self.id_lebale)
        layout.addWidget( self.copy_button )

        self.setLayout(layout)
    
        self.copy_button.clicked.connect( self.copy_text )
        
    def copy_text(self):
        pyperclip.copy( self.editor_id )

    def set_editor_id( self , text_id ):
        self.id_lebale.setText( text_id )
        self.editor_id = text_id
