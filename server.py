import logging
import threading
from server.base import engine, Base
from server.model import User, Document
from server.loop import ThreadedTCPServer, ThreadedTCPRequestHandler

HOST = '0.0.0.0'
PORT = 5000

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        print(f"Server loop running in thread: {server_thread.name}")

        server_thread.join()
        server.shutdown()
