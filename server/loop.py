import logging
import msgpack
import socketserver
import threading

class ThreadedTCPServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        """Initialize the server and keep a set of registered clients."""
        super().__init__(server_address, RequestHandlerClass, True)
        self.clients = set()
    
    def add_client(self, client):
        """Register a client with the internal store of clients."""
        logging.info(f"Connection from {client.client_address} has been established")
        self.clients.add(client)
    
    def remove_client(self, client):
        """Remove a client from the store of clients."""
        logging.info(f"Connection from {client.client_address} has been dropped")
        self.clients.remove(client)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
    
    def setup(self):
        super().setup()
        self.server.add_client(self)

    def handle(self):
        unpacker = msgpack.Unpacker()
        while True:

            buf = self.request.recv(1024**2)
            if not buf:
                break

            unpacker.feed(buf)

            for o in unpacker:
                for client in self.server.clients:
                    if client is not self:
                        client.request.sendall(msgpack.packb(o))
    
    def finish(self):
        super().finish()
        self.server.remove_client(self)

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 5000

    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"Server loop running in thread: {server_thread.name}")
        server_thread.join()
        server.shutdown()
