import random
import time

import zmq

def main():

    ctx = zmq.Context()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')
    subscriber.connect("tcp://localhost:5557")
    publisher = ctx.socket(zmq.PUSH)
    publisher.connect('tcp://localhost:5558')

    random.seed(time.time())
    while True:
        if subscriber.poll(100) & zmq.POLLIN:
            message = subscriber.recv()
            print('I: received message ', message)
        else:
            rand = random.randint(1, 100)
            if rand < 10:
                publisher.send(b"%d" % rand)
                print("I: sending message ", rand)

if __name__ == '__main__':
    main()