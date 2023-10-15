import socketserver

# {CHAT#1} Create a DB to register all client's socket information
group_queue = []

class MyUDPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        RecvData = self.request[0].strip()
        RecvSocket = self.request[1]

        RecvCmd = RecvData.decode('utf-8')
        # {CHAT#2} Command line protocol to client registration and deregistration
        # 보낸 메세지가 reg/dereg/quit인지 명령을 이해하기 위한 명령체계를 스스로 정의하고 구현해야 함.
        print('RecvCmd: ', RecvCmd)
        if RecvCmd[0] == '#' or RecvCmd == 'quit':
            if RecvCmd == '#REG':
                print('> client registered', self.client_address)
                group_queue.append(self.client_address)
            elif RecvCmd == "#DEREG" or RecvCmd == "quit":
                if group_queue.__contains__(self.client_address) == True:
                    print('> client de-registered', self.client_address)
                    group_queue.remove(self.client_address)
        else: # #이나 quit을 포함하지 않은, 등록 목적이 아닌, 일반 메세지 내용
            # {CHAT#3} Prohibit an un-registered client message
            if len(group_queue) == 0:
                print('> no clients to echo')
            elif group_queue.__contains__(self.client_address) == False:
                print('> ignores a message from un-registered client')
            else:
                # {CHAT#4} Forward a client message to whole clients (currently a broadcast)
                print('> received (', RecvData.decode('utf-8'), ') and echoed to ', len(group_queue), 'clients')
                for clientConn in group_queue:
                    RecvSocket.sendto(RecvData,clientConn)
            # [==end==]

if __name__ == "__main__":
    HOST, PORT = '127.0.0.1', 65456
    print('> echo-server is activated')
    # Create the server, binding to localhost on port 65456
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
    print('> echo-server is de-activated')