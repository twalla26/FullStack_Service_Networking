# 1:N TCP 소켓 프로그래밍
# 동시 지원 가능한 client는 1개
# 다른 client들은 서비스 중인 client 종료시까지 대기함
import socketserver

class MyTCPSocketHandler(socketserver.BaseRequestHandler):
    """
    The Request Handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the client.
    """
    def handle(self): 
        print('> client connected by IP address {0} with Port number {1}'.format(self.client_address[0], self.client_address[1]))
        while True:
            # [=start=]
            RecvData = self.request.recv(1024)
            print('> echoed:', RecvData.decode('utf-8'))
            self.request.sendall(RecvData)
            if RecvData.decode('utf-8') == 'quit':
                break
            # [==end==]

if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 65456
    print('> echo-server is activated')
    # Create the server, binding to localhost on port 62064
    with socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler) as server: # 서버 생성
        # Activate the server; this will keep running until you interrupt the program with Ctrl-C
        server.serve_forever() 
    print('> echo-server is de-activated')