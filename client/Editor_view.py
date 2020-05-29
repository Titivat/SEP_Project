from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from PySide2.QtGui import *
from diff_match_patch import diff_match_patch
from .Editor import Editor
from .Message_dialog import Message_dialog
import logging
import msgpack
import sys
import os 
from random import randint

logging.basicConfig(level=logging.INFO)

dmp = diff_match_patch()

class Editor_view(QWidget):
    def __init__(self, parent=None ,socket = None ):
        QWidget.__init__(self, parent)
        self.socket = socket

        self.setGeometry(400, 500, 1000, 500)

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

        self.open_file_action = QAction(QIcon(os.path.join('client/images', 'blue-folder-open-document.png')), "Open file...", self)
        self.open_file_action.setStatusTip("Open file")
        self.open_file_action.setShortcut( "Ctrl+o")
        file_menu.addAction( self.open_file_action)
        file_toolbar.addAction( self.open_file_action )

        self.save_file_action = QAction(QIcon(os.path.join('client/images', 'disk.png')), "Save", self)
        self.save_file_action.setStatusTip("Save current page")
        self.save_file_action.setShortcut( "Ctrl+s")
        file_menu.addAction( self.save_file_action )
        file_toolbar.addAction( self.save_file_action )

        self.saveas_file_action = QAction(QIcon(os.path.join('client/images', 'disk--pencil.png')), "Save As...", self)
        self.saveas_file_action.setStatusTip("Save current page to specified file")
        self.saveas_file_action.setShortcut( "Ctrl+Shift+s")
        file_menu.addAction( self.saveas_file_action )
        file_toolbar.addAction( self.saveas_file_action )

        self.print_action = QAction(QIcon(os.path.join('client/images', 'printer.png')), "Print...", self)
        self.print_action.setStatusTip("Print current page")
        self.print_action.setShortcut( "Ctrl+p")
        file_menu.addAction( self.print_action)
        file_toolbar.addAction( self.print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.tool_bar.addWidget(edit_toolbar)
        edit_menu = self.menu_bar.addMenu("&Edit")

        self.undo_action = QAction(QIcon(os.path.join('client/images', 'arrow-curve-180-left.png')), "Undo", self)
        self.undo_action.setStatusTip("Undo last change")
        self.undo_action.setShortcut( "Ctrl+z")
        edit_toolbar.addAction( self.undo_action )
        edit_menu.addAction( self.undo_action )

        self.redo_action = QAction(QIcon(os.path.join('client/images', 'arrow-curve.png')), "Redo", self)
        self.redo_action.setStatusTip("Redo last change")
        self.redo_action.setShortcut( "Ctrl+y")
        edit_toolbar.addAction( self.redo_action)
        edit_menu.addAction( self.redo_action)

        edit_menu.addSeparator()

        self.cut_action = QAction(QIcon(os.path.join('client/images', 'scissors.png')), "Cut", self)
        self.cut_action.setStatusTip("Cut selected text")
        self.cut_action.setShortcut( "Ctrl+x")
        edit_toolbar.addAction( self.cut_action)
        edit_menu.addAction( self.cut_action)

        self.copy_action = QAction(QIcon(os.path.join('client/images', 'document-copy.png')), "Copy", self)
        self.copy_action.setStatusTip("Copy selected text")
        self.copy_action.setShortcut( "Ctrl+c")
        edit_toolbar.addAction( self.copy_action)
        edit_menu.addAction( self.copy_action)

        self.paste_action = QAction(QIcon(os.path.join('client/images', 'clipboard-paste-document-text.png')), "Paste", self)
        self.paste_action.setStatusTip("Paste from clipboard")
        self.paste_action.setShortcut( "Ctrl+p")
        edit_toolbar.addAction( self.paste_action)
        edit_menu.addAction( self.paste_action)

        self.select_action = QAction(QIcon(os.path.join('client/images', 'selection-input.png')), "Select all", self)
        self.select_action.setStatusTip("Select all text")
        self.select_action.setShortcut( "Ctrl+a")
        edit_menu.addAction( self.select_action)

        edit_menu.addSeparator()

        run_toolbar = QToolBar("Run")
        run_toolbar.setIconSize(QSize(14, 14))
        self.tool_bar.addWidget( run_toolbar )
        run_menu = self.menu_bar.addMenu("&Run")

        self.debug_action = QAction(QIcon( os.path.join('client/images', 'run_icon.png')), "debug", self)
        self.debug_action.setStatusTip("debug")
        self.debug_action.setShortcut( "F5")
        run_menu.addAction( self.debug_action )
        run_toolbar.addAction( self.debug_action )

        text_id = QToolBar("Text Id")
        text_id.setIconSize(QSize(14, 14))
        self.tool_bar.addWidget( text_id )
        text_id = self.menu_bar.addMenu("&Text Id")
        
        self.show_id = QAction(QIcon( os.path.join('client/images', 'show_id.jpg')), "show id", self )
        self.show_id.setStatusTip("show id")
        self.show_id.setShortcut( "Ctrl+i")
        
        text_id.addAction( self.show_id )
       
        back_to_menu = QToolBar("back to menu")
        back_to_menu.setIconSize(QSize(14, 14))
        self.tool_bar.addWidget( back_to_menu )
        back_to_menu = self.menu_bar.addMenu("&back_to_menu")

        self.menu = QAction(QIcon( os.path.join('client/images', 'back.png')), "menu", self )
        self.menu.setStatusTip("menu")
        self.menu.setShortcut( "Ctrl+m")

        back_to_menu.addAction( self.menu )
        
        layout = QVBoxLayout()
        layout.addWidget( self.menu_bar )
        layout.addWidget( self.tool_bar )
        layout.addWidget( self.editor )
        layout.addWidget( self.console )

        self.setLayout(layout)      
