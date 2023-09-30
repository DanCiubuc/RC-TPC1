import socket
import sys



# TODO:
# - Fazer vars globais
# - Deixar os if else mais eficientes e bonitos
#

msgFromClient = "Hello UDP Server"
bytesToSend   = str.encode(msgFromClient)
bufferSize    = 2048
serverName    = "localhost"
clientPort    = 12000
server_name   = sys.argv[1]

UDP_Sport     = sys.argv[2]
OPEN          = "open"
CLOSE         = "close"
GET           = "get"
PUT           = "put"
EXCEPTION_1   = "(1) invalid number of arguments;"
ACK           = "ack"
CLIENT_CLOSED = "Client closed"
TCP_RUNNING   = "TCP Client is running"
CONNECTED_BY  = "Connected by: "
READ_BINARY   = "rb"
WRITE_BINARY  = "wb"
FILE_NOT_FOUND = "(2) the indicated file does not exist on the client;"

serverAddressPort = ("127.0.0.1", int(UDP_Sport))

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while True:
    args = input()

    args = args.split(" ")

    command = args[0]

    if command == OPEN:
        if len(args) != 2:
            raise Exception(EXCEPTION_1)

        bytesToSend = (" ".join(str(element) for element in args)).encode()
        clientPort = int(args[1])
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        response = UDPClientSocket.recvfrom(bufferSize)
        print(response[0].decode())

    elif command == CLOSE:
        if len(args) != 1:
            raise Exception(EXCEPTION_1)
        bytesToSend = str(args[0]).encode()

        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        response = UDPClientSocket.recvfrom(bufferSize)
        print(response[0].decode())

        UDPClientSocket.close()

        sys.exit(CLIENT_CLOSED)

    elif command == GET:
        if len(args) != 3:
            raise Exception(EXCEPTION_1)

        fileName = args[2]

        bytesToSend = (" ".join(str(element) for element in args)).encode()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        response = UDPClientSocket.recvfrom(bufferSize)

        print(response[0])

        if response[0].decode() == ACK:
            # Create TCP Welcoming socket
            TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCPSocket.bind(("", clientPort))

            # Begin Listening for incoming TCP Requests
            TCPSocket.listen(1)

            connSocket, addr = TCPSocket.accept()

            print(TCP_RUNNING)

            print(CONNECTED_BY, str(addr))  # new socket created on return

            with open(fileName, WRITE_BINARY) as file:
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
    elif command == PUT:
        if len(args) != 3:
            raise Exception(EXCEPTION_1)

        fileName = args[1]

        bytesToSend = (" ".join(str(element) for element in args)).encode()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        response = UDPClientSocket.recvfrom(bufferSize)

        print(response[0].decode())

        if response[0].decode() == ACK:
            # Create TCP Welcoming socket
            TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCPSocket.bind(("", clientPort))

            # Begin Listening for incoming TCP Requests
            TCPSocket.listen(1)

            connSocket, addr = TCPSocket.accept()

            print(TCP_RUNNING)

            print(CONNECTED_BY, str(addr))  # new socket created on return
            try:
                with open(fileName, READ_BINARY) as file:
                    while True:
                        bytesToSend = file.read(bufferSize)  # Read bytes in chunks
                        if not bytesToSend:
                            break  # No more bytes to send
                        connSocket.send(bytesToSend)
            except FileNotFoundError:
                raise Exception(FILE_NOT_FOUND)

            # Close Sockets
            connSocket.close()
            TCPSocket.close()
