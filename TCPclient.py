import socket
import sys

msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
serverName          = "localhost"

UDP_Sport = sys.argv[1]    
server_name = sys.argv[2]


 # Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while(True):

   args = input()

   args = args.split(" ")
          
   command = args[0]

   if command == "open":
       if len(args) != 2:
          raise Exception("(1) invalid number of arguments;")

       bytesToSend = (" ".join(str(element) for element in args)).encode()

   elif command == "close":
        if len(args) != 1:
            raise Exception("(1) invalid number of arguments;")
        bytesToSend = str(args[0]).encode()

   elif command == "get":
        print(args)
   elif command == "put":
        if len(args) != 2:
            raise Exception("(1) invalid number of arguments;")
        bytesToSend = (" ".join(str(element) for element in args)).encode()

   UDPClientSocket.sendto(bytesToSend, serverAddressPort)
   response = UDPClientSocket.recvfrom(bufferSize)
   print(response[0].decode())

   if(command == "put" and response[0].decode() == "ack"):
        #Create TCP Socket
        TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPClientSocket.connect((serverName, 12000)) #Open TCP connection

        print("TCP Client is running")

        fileName = args[1]

        with open(fileName, "rb") as file:
            while True:
                bytesToSend = file.read(bufferSize) #Read bytes in chunks
                if not bytesToSend:
                    break #No more bytes to send
                TCPClientSocket.send(bytesToSend)
        # Close the client socket
        TCPClientSocket.close()



# Send to server using created UDP socket
