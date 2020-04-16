import random
import time
import zmq
import pickle
from datetime import datetime
        
if __name__ == '__main__':
    context = zmq.Context()
    socket_push = context.socket(zmq.PUSH)
    socket_sub = context.socket(zmq.SUB)
    socket_push.connect('tcp://127.0.0.1:5557')
    socket_sub.connect('tcp://127.0.0.1:5558')

    socket_sub.subscribe('')

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        message = pickle.dumps( current_time )
        print('Sending:', message)
        socket_push.send(message)

        time.sleep( 2 )
        
