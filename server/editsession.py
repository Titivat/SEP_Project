import datetime
import msgpack
from .base import Session, SafeSession
from .model import User, Document
from diff_match_patch import diff_match_patch
import os
import subprocess


class EditSession:
    """Session for handling document edit"""

    dmp = diff_match_patch()

    def __init__(self, docid):
        self.clients = set()
        self.db = SafeSession()
        self.running = False
        self.doc = self.db.query(Document).filter(Document.id==docid).first()
    
    def register(self, socket):
        self.clients.add(socket)
    
    def unregister(self, socket):
        self.clients.remove(socket)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
    
    def update_text(self, socket, patch):
        patches = EditSession.dmp.patch_fromText(patch)
        if not self.doc.content:
            text, _ = EditSession.dmp.patch_apply(patches, "")
        else:
            text, _ = EditSession.dmp.patch_apply(patches, self.doc.content)
        
        self.doc.content = text

        self.broadcast(socket, msgpack.packb({"success": True, "ctx": "edit", "patch": patch}))
    
    def content(self):
        return self.doc.content
    
    def broadcast(self, socket, data, all=False):
        for client in self.clients:
            if not all:
                if client is socket:
                    continue
            client.request.sendall(data)

    def execute(self, socket):
        if self.running:
            return
        self.running = True

        filename = str(datetime.datetime.now().timestamp())+".py"
        with open(filename, "w") as f:
            f.write(self.doc.content)
        proc = subprocess.Popen(["python", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        os.remove(filename)
        output = {"ctx": "execute"}
        if stdout:
            output["success"] = True
            output["stdout"] = stdout.decode("utf-8")
        if stderr:
            output["success"] = False
            output["stderr"] = stderr.decode("utf-8")
        
        self.broadcast(socket, msgpack.packb(output), all=True)

        self.running = False
