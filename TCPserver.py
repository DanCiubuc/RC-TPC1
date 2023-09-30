import socket
import sys
import os

localIP    = "127.0.0.1"
bufferSize = 2048
clientPort = 12000
serverName = "localhost"

UDP_Sport    = int(sys.argv[1])
UDP_RUNNING  = "UDP server up and listening"
TCP_RUNNING  = "TCP Socket is running"
OPEN         = "open"
CLOSE        = "close"
GET          = "get"
PUT          = "put"
SERVER       = "server"
ACK          = "ack"
READ_BINARY  = "rb"
WRITE_BINARY = "wb"
CLOSE_SOCKET = "i want to close client socket"
NACK_3       = "nack 3"

# TODO: reutilizar código para get e put (colocar um if)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, UDP_Sport))

print(UDP_RUNNING)

# Listen for incoming datagrams
while True:
    try:
        # if os not exists ....
        clientMsg = UDPServerSocket.recvfrom(bufferSize)

        args = (clientMsg[0].decode()).split(" ")

        command = args[0]

        if command == OPEN:
            clientPort = int(args[1])

            UDPServerSocket.sendto(ACK.encode(), clientMsg[1])
        elif command == CLOSE:
            UDPServerSocket.sendto(ACK.encode(), clientMsg[1])
        elif command == GET:
            fileName = args[1]

            if not (os.path.exists(fileName)):
                # File doesn't exist in the server's file system
                UDPServerSocket.sendto(NACK_3.encode(), clientMsg[1])
            else:
                # File exists in the server's file system
                UDPServerSocket.sendto(ACK.encode(), clientMsg[1])
                serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverSocket.connect((serverName, clientPort))
                print(TCP_RUNNING)

                with open(os.path.join(SERVER, fileName), READ_BINARY) as file:
                    while True:
                        bytesToSend = file.read(bufferSize)  # Read bytes in chunks
                        if not bytesToSend:
                            break  # No more bytes to send
                        serverSocket.send(bytesToSend)
                # Close Sockets
                serverSocket.close()
        elif command == PUT:
            fileName = args[2]

            if (os.path.exists(fileName)):
                # File already exists in the server's file system
                UDPServerSocket.sendto(NACK_3.encode(), clientMsg[1])
            else:
                # File doesn't exist in the server's file system
                UDPServerSocket.sendto(ACK.encode(), clientMsg[1])

                serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverSocket.connect((serverName, clientPort))

                print(TCP_RUNNING)
                print(fileName)

                with open(os.path.join(SERVER, fileName), WRITE_BINARY) as file:
                    while True:
                        bytesReceived = serverSocket.recv(bufferSize) # Receives bytes in chunks
                        if not bytesReceived:
                            break  # No more bytes to receive
                        file.write(bytesReceived)
                serverSocket.close()

    except KeyboardInterrupt:
        print(CLOSE_SOCKET)
        UDPServerSocket.close()
        break
