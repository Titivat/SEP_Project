from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from menu_view import Menu_view
from document_form import Document_Form
import random
import sys

class Menu_controler( QMainWindow ):

    def __init__( self ):
        QMainWindow.__init__(self, None)

        self.ui = Menu_view()
        self.ui.setupUi( self )

        self.load_document()

        self.ui.adddocbutton.clicked.connect( self.addDocument )

        self.show()

    def addDocument( self ): 
        new_dociment = Document_Form( self )
        self.ui.listWidget.addItem( new_dociment.getItemN() )
        self.ui.listWidget.setItemWidget( new_dociment.getItemN() , new_dociment.getWidget() )

    def load_document( self ):
        pass 
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    clinet = Menu_controler()

    sys.exit(app.exec_())

    
