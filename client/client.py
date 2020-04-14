import random
import time
import zmq

if __name__ == '__main__':
    context = zmq.Context()
    socket_push = context.socket(zmq.PUSH)
    socket_sub = context.socket(zmq.SUB)
    socket_push.connect('tcp://127.0.0.1:5557')
    socket_sub.connect('tcp://127.0.0.1:5558')

    socket_sub.subscribe('')

    while True:
        message = '%f %d' % (time.time(), random.randint(1, 10000))
        print('Sending:', message)
        socket_push.send_string(message)
        message = socket_sub.recv_string()
        print('Received:', message)