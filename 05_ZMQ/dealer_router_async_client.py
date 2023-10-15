import zmq
import sys
import threading
import time
from random import randint, random

class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, id):
        self.id = id
        threading.Thread.__init__(self)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = u'%s' % self.id
        socket.identity = identity.encode('ascii')
        socket.connect('tcp://localhost:5570')
        print('Client %s started' % (identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0

        while True:
            reqs = reqs + 1
            print('Req #%d sent..' % (reqs))
            socket.send_string(u'request #%d' % (reqs))

            time.sleep(1)
            sockets = dict(poll.poll(1000))
            if socket in sockets:
                msg = socket.recv()
                print('{0} received: {1}'.format(identity, msg))
            
        socket.close()
        context.term()

def main(argv):
    """main function"""
    client = ClientTask(argv[1])
    client.start()

if __name__ == '__main__':
    main(sys.argv)