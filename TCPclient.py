import socket
import sys

msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

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
        print(args)

   UDPClientSocket.sendto(bytesToSend, serverAddressPort)
   response = UDPClientSocket.recvfrom(bufferSize)
   print(response[0].decode())


# Send to server using created UDP socket
