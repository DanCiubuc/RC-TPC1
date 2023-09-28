import socket

import sys

localIP     = "127.0.0.1"
bufferSize  = 1024
serverPort = 12000
sockBuffer = 2048

UDP_Sport = int(sys.argv[1])   

 # Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 # Bind to address and ip
UDPServerSocket.bind((localIP, UDP_Sport))

print("UDP server up and listening")

 # Listen for incoming datagrams
while(True):
    TCP_port = default_TCP
    clientMsg = UDPServerSocket.recvfrom(bufferSize)
        
    args = (clientMsg[0].decode()).split(" ")
          
    command = args[0]
        
    if command == "open":
        TCP_port = args[1]
        
        UDPServerSocket.sendto("ack".encode(), clientMsg[1])
    elif command == "close":
        print(args)
    elif command == "get":
        print(args)
    elif command == "put":
        print(args)
   

