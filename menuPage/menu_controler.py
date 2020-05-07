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

        self.load_my_document()

        self.ui.adddocbutton.clicked.connect( self.addDocument )
        self.ui.mydrivebutton.clicked.connect( self.my_drive )
        self.ui.sharedrivebutton.clicked.connect( self.load_share_drive )
        self.ui.logoutbutton.clicked.connect( self.log_out )

        self.show()

    def my_drive( self ):
        self.load_my_document()

        _translate = QCoreApplication.translate
        self.ui.pagestatus.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; font-weight:600;\">My Drive</span></p></body></html>"))

    def load_share_drive( self ):
        self.load_share_document()

        _translate = QCoreApplication.translate
        self.ui.pagestatus.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; font-weight:600;\">Share Drive</span></p></body></html>"))

    def addDocument( self ): 
        document_name, add = QInputDialog.getText(self, 'add', 'Enter Document name')

        if not add:
            pass
        else:
            new_dociment = Document_Form( self  )
            new_dociment.set_document_name( document_name )
            self.ui.listWidget.addItem( new_dociment.getItemN() )
            self.ui.listWidget.setItemWidget( new_dociment.getItemN() , new_dociment.getWidget() )
    
    def log_out( self ):
        self.close()

    def load_my_document( self ):
        pass 

    def load_share_document( self ):
        pass
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    clinet = Menu_controler()

    sys.exit(app.exec_())

    
