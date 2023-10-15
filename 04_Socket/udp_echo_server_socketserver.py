import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socekt, and since
    there is no connection, the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        # [=start=]
        RecvData = self.request[0].strip()
        RecvSocket = self.request[1]
        print(RecvData, RecvSocket)
        print('> echoed:', RecvData.decode('utf-8'))
        RecvSocket.sendto(RecvData, self.client_address)
        print(self.client_address)
        # [==end==]

if __name__ == "__main__":
    HOST, PORT = '127.0.0.1', 65456
    print('> echo-server is activated')
    # Create the server, binding to localhost on port 65456
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
    print('> echo-server is de-activated')