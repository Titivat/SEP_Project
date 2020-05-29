import datetime
import msgpack
from server.base import Session
from server.model import User, Document
from diff_match_patch import diff_match_patch
from .response import Response
import os
import subprocess


class EditSession:
    """Session for handling document edit"""

    dmp = diff_match_patch()

    def __init__(self, docid):
        self.clients = set()
        self.docid = docid
        self.running = False

        db = Session()
        doc = db.query(Document).filter(Document.id==docid).first()
        self.text = doc.content
        db.close()
    
    def register(self, socket):
        self.clients.add(socket)
    
    def unregister(self, socket, db):
        self.clients.remove(socket)
        try:
            doc = db.query(Document).filter(Document.id==self.docid).first()
            doc.content = self.text
            db.commit()
        except Exception:
            db.rollback()
    
    def update_text(self, socket, patch):
        response = Response("edit")

        patches = EditSession.dmp.patch_fromText(patch)
        if not self.text:
            text, _ = EditSession.dmp.patch_apply(patches, "")
        else:
            text, _ = EditSession.dmp.patch_apply(patches, self.text)
        
        self.text = text

        self.broadcast(socket, response(patch=patch))
    
    def content(self):
        return self.text
    
    def broadcast(self, socket, data, all=False):
        for client in self.clients:
            if not all:
                if client is socket:
                    continue
            client.request.sendall(data)

    def execute(self, socket):
        response = Response("execute")

        if self.running:
            return
        self.running = True

        filename = str(datetime.datetime.now().timestamp())+".py"
        with open(filename, "w") as f:
            f.write(self.text)
        proc = subprocess.Popen(["python", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        os.remove(filename)

        if stdout:
            self.broadcast(socket, response(stdout=stdout.decode("utf-8")), all=True)
        else:
            self.broadcast(socket, response(False, stderr=stderr.decode("utf-8")), all=True)

        self.running = False
