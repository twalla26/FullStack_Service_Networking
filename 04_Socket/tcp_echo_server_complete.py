import socket

HOST = '127.0.0.1'
PORT = 65456

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        try: # 예외처리를 하기위한 try 문
            if serverSocket.bind((HOST, PORT)) == -1: # 만약 bind 함수가 실패해서 -1을 반환하면
                print('> bind() failed and program terminated') # 그렇다고 알려줌.
                serverSocket.close()
                return
        except Exception as exceptionObj: # 에러 받아서 무슨 에러인지 출력
            print('> bind() failed by exception:', exceptionObj)
            serverSocket.close()
            return
        
        if serverSocket.listen() == -1: # listen 함수 에러
            print('> listen() failed and program terminated')
            serverSocket.close()
            return
        
        clientSocket, clientAddress = serverSocket.accept()

        with clientSocket:
            print('> client connected by IP address {0} with Port number {1}'.format(clientAddress[0], clientAddress[1]))
            while True:
                # [=start=]
                RecvData = clientSocket.recv(1024) # 클라에게 받은 데이터 저장
                print('> echoed:', RecvData.decode('utf-8')) # 그대로 출력
                clientSocket.sendall(RecvData)
                if RecvData.decode('utf-8') == 'quit':
                    break
                # [==end==]

if __name__ == '__main__':
    print('> echo-server is activated')
    main()
    print('> echo-server is de-activated')