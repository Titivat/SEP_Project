from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from PySide2.QtGui import *
from diff_match_patch import diff_match_patch
from .Editor_view import Editor_view
from .Message_dialog import Message_dialog
import logging
import msgpack
import time
import sys
import os 
from random import randint

logging.basicConfig(level=logging.INFO)
dmp = diff_match_patch()

class Editor_control(QWidget):
    def __init__( self , socket ):
        super( Editor_control , self).__init__()
        self.socket = socket
        
        self.text_edit_id = None 

        self.path = None 

        self.unpacker = msgpack.Unpacker()
        
        self.setGeometry(0, 0, 800, 400)

        self.unpacker = msgpack.Unpacker()

        self.editor = Editor_view( self ,self.socket )
        self.editor.editor.change_evt.connect( self.on_change )

        self.editor.redo_action.triggered.connect(self.editor.editor.redo)
        self.editor.select_action.triggered.connect(self.editor.editor.selectAll )
        self.editor.cut_action.triggered.connect(self.editor.editor.cut)
        self.editor.copy_action.triggered.connect( self.editor.editor.copy )
        self.editor.paste_action.triggered.connect(self.editor.editor.paste)
        self.editor.print_action.triggered.connect(self.file_print)
        self.editor.menu.triggered.connect( self.back_to_menu )
        self.editor.show_id.triggered.connect( self.show_id_message )
        self.editor.save_file_action.triggered.connect( self.file_save )
        self.editor.open_file_action.triggered.connect( self.file_open )
        self.editor.debug_action.triggered.connect( self.start_debuging )
        self.editor.undo_action.triggered.connect(self.editor.editor.undo)
        self.editor.saveas_file_action.triggered.connect( self.file_saveas )
       
        layout = QVBoxLayout()
        layout.addWidget( self.editor )

        self.setLayout(layout)

    def set_text_id( self , text_id ):
        self.text_edit_id = text_id

    def back_to_menu( self ):
        self.socket.write(msgpack.packb({"action":"close" })) 

    def closeEvent(self, event):
        self.back_to_menu()
        event.accept()
        
    def connect(self, host, port):
        self.socket.connectToHost(host, port, QIODevice.ReadWrite)
    
    def on_read(self):
        instr = QDataStream(self.socket)
        instr.setVersion(QDataStream.Qt_5_0)
        buf = instr.readRawData(1024**2)
        if not buf:
            return
        self.unpacker.feed(buf)
        for data in self.unpacker:
            logging.info(f"[SERVER] {data}")
            self.editor.editor.update_text(data)

    def on_error(self, socketError):
        logging.error(socketError)
        self.dialog_message("socket error")
   
    def show_id_message( self ):
        print( self.text_edit_id )
        message_dialog = Message_dialog( self )
        message_dialog.set_editor_id( self.text_edit_id )
        message_dialog.show()

    def on_change(self, diff):
        bin = msgpack.packb({"action":"edit", "patch": diff}, use_bin_type=True)
        self.socket.write(bin)

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt)")

        try:
            with open(path, 'rU') as f:
                text = f.read()

        except Exception as e:
            self.dialog_message(str(e))

        else:
            self.path = path
            self.editor.editor.clear()
            self.editor.editor.insertPlainText(text)

            self.update_textEditor()

    def file_save(self):
        if self.path is None:
            return self.file_saveas()

        text = self.editor.editor.toPlainText()

        try:
            with open(self.path, 'w') as f:
                f.write(text)

            self.dialog_message("Sucessfully save")

        except Exception as e:
            self.dialog_message(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);")

        if not path:
            return

        text = self.editor.editor.toPlainText()

        try:
            with open(path, 'w') as f:
                f.write(text)

            self.dialog_message("Sucessfully saves")

        except Exception as e:
            self.dialog_message(str(e))
             
        else:
            self.path = path

    def dialog_message(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.show()

    def update_textEditor( self ):
        updated_text = self.editor.editor.toPlainText()

        patches = dmp.patch_make(self.editor.editor.text, updated_text)
        diff = dmp.patch_toText(patches)

        self.editor.editor.text = updated_text

        self.editor.editor.change_evt.emit(diff)

    
    def start_debuging( self ):
        self.socket.write(msgpack.packb({"action": "execute"}))

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())
