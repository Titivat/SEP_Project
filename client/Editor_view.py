from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from PySide2.QtGui import *
from diff_match_patch import diff_match_patch
from .Editor import Editor
import logging
import msgpack
import sys
import os 
from random import randint

logging.basicConfig(level=logging.INFO)

dmp = diff_match_patch()
FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

class Editor_view(QWidget):
    def __init__(self, parent=None ,socket = None ):
        QWidget.__init__(self, parent)
        self.socket = socket

        self.text_edit_id = None 
 
        self.setGeometry(400, 400, 800, 400)

        self.unpacker = msgpack.Unpacker()

        self.editor = Editor( self.socket )
        self.editor.setTabStopWidth( self.editor.fontMetrics().width(' ') * 4)

        self.console = QPlainTextEdit()
        self.console.setMaximumSize( 1000 , 100 )
        self.console.setReadOnly( True )
        
        self.menu_bar = QMenuBar( self )
        self.tool_bar = QToolBar( self ) 

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize( QSize(14, 14) )
        self.tool_bar.addWidget(file_toolbar)
        file_menu = self.menu_bar.addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join('client/images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.setShortcut( "Ctrl+o")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('client/images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.setShortcut( "Ctrl+s")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('client/images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.setShortcut( "Ctrl+Shift+s")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('client/images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.setShortcut( "Ctrl+p")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.tool_bar.addWidget(edit_toolbar)
        edit_menu = self.menu_bar.addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join('client/images', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.setShortcut( "Ctrl+z")
        undo_action.triggered.connect(self.editor.undo)
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('client/images', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.setShortcut( "Ctrl+y")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('client/images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut( "Ctrl+x")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('client/images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.setShortcut( "Ctrl+c")
        copy_action.triggered.connect( self.editor.copy )
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('client/images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.setShortcut( "Ctrl+p")
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('client/images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.setShortcut( "Ctrl+a")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        run_toolbar = QToolBar("Run")
        run_toolbar.setIconSize(QSize(14, 14))
        self.tool_bar.addWidget( run_toolbar )
        run_menu = self.menu_bar.addMenu("&Run")

        debug_action = QAction(QIcon( os.path.join('client/images', 'run_icon.png')), "debug", self)
        debug_action.setStatusTip("debug")
        debug_action.setShortcut( "F5")
        debug_action.triggered.connect( self.start_debuging )
        run_menu.addAction( debug_action )
        run_toolbar.addAction( debug_action )

        text_id = QToolBar("Text Id")
        text_id.setIconSize(QSize(14, 14))
        self.tool_bar.addWidget( text_id )
        text_id = self.menu_bar.addMenu("&Text Id")
        
        show_id = QAction(QIcon( os.path.join('client/images', 'show_id.jpg')), "show id", self )
        show_id.setStatusTip("show id")
        show_id.setShortcut( "Crt+i")
        show_id.triggered.connect( self.show_id )
        text_id.addAction( show_id )
        text_id.addAction( show_id )

        layout = QVBoxLayout()
        layout.addWidget( self.menu_bar )
        layout.addWidget( self.tool_bar )
        layout.addWidget( self.editor )
        layout.addWidget( self.console )

        self.setLayout(layout)

    def show_id( self ):
        self.dialog_critical( self.text_edit_id )

    def set_text_id( self , text_id ):
        self.text_edit_id = text_id
    
    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
    
    def start_debuging( self ):
        self.socket.write(msgpack.packb({"action": "execute"}))

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

        try:
            with open(path, 'rU') as f:
                text = f.read()

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            # Qt will automatically try and guess the format as txt/html
            self.editor.editor.setText(text)
            self.update_title()

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        text = self.editor.editor.toHtml() if splitext(self.path) in HTML_EXTENSIONS else self.editor.editor.toPlainText()

        try:
            with open(self.path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        text = self.editor.editor.toHtml() if splitext(path) in HTML_EXTENSIONS else self.editor.editor.toPlainText()

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.editor.print_(dlg.printer())

