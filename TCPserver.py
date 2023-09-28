import socket
import sys
import os

localIP = "127.0.0.1"
bufferSize = 2048
clientPort = 12000
serverName = "localhost"

UDP_Sport = int(sys.argv[1])

# TODO: reutilizar código para get e put (colocar um if)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, UDP_Sport))

print("UDP server up and listening")

# Listen for incoming datagrams
while True:
    try:
        # if os not exists ....
        clientMsg = UDPServerSocket.recvfrom(bufferSize)

        args = (clientMsg[0].decode()).split(" ")

        command = args[0]

        if command == "open":
            clientPort = int(args[1])

            UDPServerSocket.sendto("ack".encode(), clientMsg[1])
        elif command == "close":
            UDPServerSocket.sendto("ack".encode(), clientMsg[1])
        elif command == "get":
            # File exists in the server's file system
            UDPServerSocket.sendto("ack".encode(), clientMsg[1])
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.connect((serverName, clientPort))
            print("TCP Socket is running")
            fileName = args[1]
            print(fileName)

            with open(os.path.join("server", fileName), "rb") as file:
                while True:
                    bytesToSend = file.read(bufferSize)  # Read bytes in chunks
                    if not bytesToSend:
                        break  # No more bytes to send
                    serverSocket.send(bytesToSend)
            # Close Sockets
            serverSocket.close()
        elif command == "put":
            FILE_Name = args[2]

            # File exists in the server's file system
            UDPServerSocket.sendto("ack".encode(), clientMsg[1])

            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.connect((serverName, clientPort))

            print("TCP Socket is running")

            fileName = args[2]
            print(fileName)

            with open(os.path.join("server", fileName), "wb") as file:
                while True:
                    bytesReceived = serverSocket.recv(
                        bufferSize
                    )  # Receives bytes in chunks
                    if not bytesReceived:
                        break  # No more bytes to receive
                    file.write(bytesReceived)
            serverSocket.close()

    except KeyboardInterrupt:
        print("i want to close client socket")
        UDPServerSocket.close()
        break
    # except Exception as e:
    #     print(e)
