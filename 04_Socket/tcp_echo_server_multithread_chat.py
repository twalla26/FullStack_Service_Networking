import socketserver
import threading

# {CHAT#1} Create a DB to register all client's socket information
group_queue = [] # 원래 전역변수 쓰면 안되지만, 임시로!

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Show a client connection information
        print('> client connected by IP address {0} with Port number {1}.'.format(self.client_address[0], self.client_address[1]))

        # {CHAT#2} Import a client DB into Request Handler
        global group_queue
        # {CHAT#3} Register a new client connection information into a client DB
        group_queue.append(self.request) # 클라이언트가 본인의 요청 정보 저장

        while True:
            # [=start=]
            RecvData = self.request.recv(1024)
            if RecvData.decode('utf-8') == 'quit':
                # {CHAT#4} Deregister a disconnected client from a client DB
                group_queue.remove(self.request)
                break
            else:
                # {CHAT#5} Forward a client message to whole clients (currently a broadcast)
                print('> received (', RecvData.decode('utf-8'), ') and echoed to ', len(group_queue), 'clients')
                for conn in group_queue:
                    conn.sendall(RecvData)
            # [==end==]

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    HOST, PORT = 'localhost', 65456
    print('> echo-server is activated')

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)

        # Set to exit the server thread when the main thread terminates, then execute the main thread
        server_thread.daemon = True
        server_thread.start()
        print('> server loop running in thread (main thread):', server_thread.name)

        # Server termination by input "quit" when all client connections are disconnected
        baseThreadNumber = threading.active_count()
        while True:
            msg = input('> ')
            if msg == 'quit':
                if baseThreadNumber == threading.active_count():
                    print("> stop procedure started")
                    break
                else:
                    print('> active threads are remained:', threading.active_count() - baseThreadNumber, 'threads')

        print('> echo-server is de-activated')
        server.shutdown()


