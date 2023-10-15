import socket

HOST = '127.0.0.1'
PORT = 65456

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:

        try:
            if clientSocket.connect((HOST, PORT)) == -1:
                print('> connect() failed and program terminated')
                clientSocket.close()
                return
            
        except Exception as exceptionObj:
            print('> connect() failed by exception:', exceptionObj)
            return
        
        while True:
            # [=start=]
            sendMsg = input("> ")
            clientSocket.sendall(bytes(sendMsg, 'utf-8'))
            recvData = clientSocket.recv(1024)
            print('> received:', recvData.decode('utf-8'))
            if sendMsg == 'quit':
                break
            # [==end==]

if __name__ == '__main__':
    print('> echo-client is activated')
    main()
    print('> echo-client is de-activated')
