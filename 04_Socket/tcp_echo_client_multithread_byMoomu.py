import socket
import threading

HOST = '127.0.0.1'
PORT = 65456

print('> echo-client is activated')

def recv_handler(client):
    while True:
        recvData = clientSocket.recv(32) # 서버로부터 받은 데이터, 1024 바이트만큼 받음.
        print('> received:', recvData.decode('utf-8')) # 받은거 디코딩해서 출력

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket: # 클라 소켓 생성
    clientSocket.connect((HOST, PORT)) # 서버에 연결 요청
    recvHandler = threading.Thread(target=recv_handler, args=(clientSocket, ))
    recvHandler.start()
    while True:
        sendMsg = input("> ") # 보낼 메세지를 사용자로부터 입력 받음.
        clientSocket.send(bytes(sendMsg, 'utf-8')) # 입력 받은 메세지를 바이트로 변환해서 서버에 전달
        if sendMsg == 'quit':
            break # 연결 해제되면 with 구문에서 나오면서 자동으로 해제됨.

print('> echo-client is deactivated')


# 이 코드는 동기식 blocking 코드이다.
# 따라서, 1024 바이트 이상을 서버로 보내면 서버는 이를 2개로 나눠서 클라에게 보낸다.
# 그런데, 동기식으로 작동하기 때문에 두 번째 메세지가 클라에 도착할 때에는 클라는 입력을 받아야 하는 상태이기에
# 클라가 두 번째 입력을 마쳐야만 기존의 두 번째 메세지가 도착하게 된다.
# 즉, 메세지가 한칸씩 밀려나서 전송되는 것이다!!\