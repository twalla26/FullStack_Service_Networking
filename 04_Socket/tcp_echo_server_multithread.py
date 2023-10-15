import socketserver
import threading

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Show a client connection informantion
        print('> client connected by IP address {0} with Port number {1}.'.format(self.client_address[0], self.client_address[1]))

        while True:
            # [=start=]
            RecvData = self.request.recv(1024)
            cur_thread = threading.current_thread() # 실행되는 스레드에 이름(숫자) 부여
            print('> echoed:', RecvData.decode('utf-8'), 'by', cur_thread.name) # + 어떤 스레드에서 온 데이터인지 출력
            self.request.sendall(RecvData)
            if RecvData.decode('utf-8') == 'quit':
                break
            # [==end==]

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # socketserver.ThreadingMaxIn --> TCP 서버가 멀티스레드 가능하게 하는 mix in 클래스.
    pass

if __name__ == '__main__':
    HOST, PORT = 'localhost', 65456
    print('> echo-server is activated')
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) # 서버 생성
    with server:
        ip, port = server.server_address

        # start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever) # 연결될 때마다 스레드 생성
        # serve_forever: 싱글 스레드에서 하나의 connection만 처리하는 애

        # Set to exit the server thread when the main thread terminates, then execute the main thread
        server_thread.daemon = True # 메인이 죽으면 스레드도 죽게 설정, 디폴트는 false
        server_thread.start() # 여기서 스레드 시작!
        print('> server loop running in thread (main thread):', server_thread.name)

        # Server termination by input "quit" when all client connections are disconnected
        # 서버는 로그 파일에 클라의 ip 등의 계속해서 기록하는데,
        # 이때, blocked system으로, 어느 정도 기록이 쌓여야 메모리에서 디스크로 이동됨.
        # 따라서, 서버가 갑자기 죽지 않고, 하나씩 예쁘게 죽어야 정보가 다 디스크로 전송되어 문제가 없음.
        baseThreadNumber = threading.active_count() # 서버 시작 후이므로 baseThreadNumber는 1이 됨.
        while True:
            msg = input('> ')
            if msg == 'quit':
                if baseThreadNumber == threading.active_count():
                    print('> stop procedure started')
                    break
                else:
                    print('> active threads are remained :', threading.active_count() - baseThreadNumber, "threads")

        print('> echo-server is de-activated')
        server.shutdown()
    