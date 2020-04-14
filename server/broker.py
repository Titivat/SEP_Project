import random
import time
import zmq

if __name__ == '__main__':
    context = zmq.Context()
    socket_pull = context.socket(zmq.PULL)
    socket_pub = context.socket(zmq.PUB)
    socket_pull.bind('tcp://*:5557')
    socket_pub.bind('tcp://*:5558')

    while True:
        message = socket_pull.recv_string()
        print('Received:', message)
        print('Sending:', message)
        socket_pub.send_string(message)
        time.sleep(0.5)