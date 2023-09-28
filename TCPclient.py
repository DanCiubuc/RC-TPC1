import socket
import sys

msgFromClient = "Hello UDP Server"

# TODO:
# - Fazer vars globais
# - Deixar os if else mais eficientes e bonitos
#


bytesToSend = str.encode(msgFromClient)

bufferSize = 2048
serverName = "localhost"
clientPort = 12000

server_name = sys.argv[1]

UDP_Sport = sys.argv[2]
serverAddressPort = ("127.0.0.1", int(UDP_Sport))


# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while True:
    args = input()

    args = args.split(" ")

    command = args[0]

    if command == "open":
        if len(args) != 2:
            raise Exception("(1) invalid number of arguments;")

        bytesToSend = (" ".join(str(element) for element in args)).encode()
        clientPort = int(args[1])
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        response = UDPClientSocket.recvfrom(bufferSize)
        print(response[0].decode())

    elif command == "close":
        if len(args) != 1:
            raise Exception("(1) invalid number of arguments;")
        bytesToSend = str(args[0]).encode()

        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        response = UDPClientSocket.recvfrom(bufferSize)
        print(response[0].decode())

        UDPClientSocket.close()

        sys.exit("Client closed")

    elif command == "get":
        if len(args) != 3:
            raise Exception("(1) invalid number of arguments;")

        file_name = args[2]

        bytesToSend = (" ".join(str(element) for element in args)).encode()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        response = UDPClientSocket.recvfrom(bufferSize)

        print(response[0])

        if response[0].decode() == "ack":
            # Create TCP Welcoming socket
            TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCPSocket.bind(("", clientPort))

            # Begin Listening for incoming TCP Requests
            TCPSocket.listen(1)

            connSocket, addr = TCPSocket.accept()

            print("TCP Client is running")

            fileName = args[2]

            print("Connected by: ", str(addr))  # new socket created on return

            with open(fileName, "wb") as file:
                while True:
                    bytesReceived = connSocket.recv(
                        bufferSize
                    )  # Receives bytes in chunks
                    if not bytesReceived:
                        break  # No more bytes to receive
                    file.write(bytesReceived)
            # Close Sockets
            connSocket.close()
            TCPSocket.close()
    elif command == "put":
        if len(args) != 3:
            raise Exception("(1) invalid number of arguments;")

        file_name = args[1]

        bytesToSend = (" ".join(str(element) for element in args)).encode()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        response = UDPClientSocket.recvfrom(bufferSize)

        print(response[0].decode())

        if response[0].decode() == "ack":
            # Create TCP Welcoming socket
            TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCPSocket.bind(("", clientPort))

            # Begin Listening for incoming TCP Requests
            TCPSocket.listen(1)

            connSocket, addr = TCPSocket.accept()

            print("TCP Client is running")

            fileName = args[1]

            print("Connected by: ", str(addr))  # new socket created on return

            with open(fileName, "rb") as file:
                while True:
                    bytesToSend = file.read(bufferSize)  # Read bytes in chunks
                    if not bytesToSend:
                        break  # No more bytes to send
                    connSocket.send(bytesToSend)
            # Close Sockets
            connSocket.close()
            TCPSocket.close()
