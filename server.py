import threading
from server.loop import ThreadedTCPServer, ThreadedTCPRequestHandler

HOST = '0.0.0.0'
PORT = 5000

if __name__ == "__main__":
    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"Server loop running in thread: {server_thread.name}")
        server_thread.join()
        server.shutdown()
