import socket
import sys
import os

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
    try:
        #TCP_port = default_TCP
        clientMsg = UDPServerSocket.recvfrom(bufferSize)
        
        args = (clientMsg[0].decode()).split(" ")
          
        command = args[0]

        
        if command == "open":
            TCP_port = args[1]
        
            UDPServerSocket.sendto("ack".encode(), clientMsg[1])
        elif command == "close":

            UDPServerSocket.sendto("ack".encode(), clientMsg[1])

        elif command == "get":
            print(args)
        elif command == "put":
            FILE_Name = args[1]

            if (os.path.exists(FILE_Name)):
                #File exists in the server's file system
                UDPServerSocket.sendto("nack 3".encode(), clientMsg[1])
            else:
                #Create TCP Welcoming socket
                TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                TCPServerSocket.bind(("", serverPort))

                #Begin Listening for incoming TCP Requests
                TCPServerSocket.listen(1)

                print("TCP Server is running")

                #File does not exist
                UDPServerSocket.sendto("ack".encode(), clientMsg[1])

                connSocket, addr = TCPServerSocket.accept()  #waits for incoming requests

                print("Connected by: ", str(addr)) #new socket created on return

                with open(FILE_Name, "wb") as file:
                    while True:
                        bytesReceived = connSocket.recv(bufferSize) #Receives bytes in chunks
                        if not bytesReceived:
                            break #No more bytes to receive
                        file.write(bytesReceived)
                #Close Sockets
                connSocket.close()
                TCPServerSocket.close()
    except KeyboardInterrupt:
        print ("i want to close client socket")
        UDPServerSocket.close()
        break
    except Exception as e:
        print(e)

