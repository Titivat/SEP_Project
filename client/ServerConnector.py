import zmq
import pickle

class ServerConnector:

    def __init__( self ):
        self.context = zmq.Context()
        self.socket_push = self.context.socket(zmq.PUSH)
        self.socket_sub = self.context.socket(zmq.SUB)
        self.socket_push.connect('tcp://127.0.0.1:5557')
        self.socket_sub.connect('tcp://127.0.0.1:5558')

        self.socket_sub.subscribe('') 

    def getMessage( self ):
        message = self.socket_sub.recv()

        if type( message ) is not bytes:
            return message
        else:
            data = pickle.loads( message )
            return data

    def sendData( self, data ):
        dumpData = pickle.dumps( data )
        self.socket_push.send( dumpData )
        