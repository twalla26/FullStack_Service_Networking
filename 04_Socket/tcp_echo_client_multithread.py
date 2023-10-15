import socket
import threading

HOST = "127.0.0.1"
PORT = 65456

# {CHAT#1} Create a separate receive handler
def recvHandler(clientSocket): # receive handler를 분리해서 만듦.
    while True:
        recvData = clientSocket.recv(1024)
        print('> received:', recvData.decode('utf-8'))
        if recvData.decode('utf-8') == 'quit':
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:

        try:
            if clientSocket.connect((HOST, PORT)) == -1: # 연결 에러
                print('> connect() failed and program terminated')
                clientSocket.close()
                return 
        except Exception as exceptionObj:
            print('> connect() failed by exception:', exceptionObj)
            return
        
        # 연결 성공 후
        # {CHAT#2} Create a receive handler and set to exit the thread, then execute the thread
        clientThread = threading.Thread(target=recvHandler, args=(clientSocket, )) 
        # 클라 소켓으로 receive 하기 위해 내가 만든 tcp 컨넥션을 인자로 전달
        clientThread.daemon = True
        clientThread.start()
        # connect 후, 서버와 마찬가지로 스레드를 띄우고 receiveHandler 하게 함.

        while True:
            # [=start=]
            sendMsg = input('> ')
            clientSocket.sendall(bytes(sendMsg, 'utf-8'))
            if sendMsg == 'quit':
                break
            # [==end==]

if __name__ == '__main__':
    print('> echo-client is activated')
    main()
    print('> echo-client is de-activated')