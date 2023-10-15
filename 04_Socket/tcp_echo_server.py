# echo server: 내가 보낸 메세지를 상대방이 잘 받았다는 의미로 그대로 다시 보낸 것, 서버가 살아있는지 확인하는 용도
import socket

HOST = '127.0.0.1'
PORT = 65456 # 서버 포트 지정

print('> echo-server is activated')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket: # socket(): 새로운 소켓 생성
    # AF_INET: 네트워크 프로토콜 IPv4, SOCK_STREAM: TCP
    serverSocket.bind((HOST, PORT)) # bind: 소켓과 주소 연결
    serverSocket.listen() # listen: 클라의 접속 대기
    clientSocket, clientAddress = serverSocket.accept() # 클라의 접속 요청 accept하면서 클라 정보 저장
    # accept(): 소켓에 누군가가 접속하여 연결되었을 때에 비로소 결과값이 return되는 함수
    with clientSocket:
        print(f'> client connected by IP address {clientAddress[0]} with Port number {clientAddress[1]}')
        while True:
            # [=start=]
            RecvData = clientSocket.recv(1024) # recv(): 소켓에 메시지가 실제로 수신될 때까지 코드 대기, 인자로 수신할 바이트 크기 지정, 소켓에서 1024byte 만큼 가져옴.
            print('> echoed:', RecvData.decode('utf-8')) # decode(): 데이터를 바이트로 수신하므로, 문자열로서 활용하기 위해서 디코딩
            clientSocket.sendall(RecvData) # 전송 받은 데이터를 그대로 다시 클라로 전송함.
            if RecvData.decode('utf-8') == 'quit': # 클라가 quit 보내면 연결 끊기
                break
            # [==end==]
print('> echo-server is de-activated')
