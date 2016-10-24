import socket
import sys


UDP_IP = 'localhost'
UDP_PORT = 12345
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (UDP_IP, UDP_PORT)

while True:
    try:
        message = input("Enter input: ")
        sent = s.sendto(message.encode(), server_address)

        print('waiting for server to respond')
        data, server = s.recvfrom(4096)
        if data:
            print('received: ', data.decode())
        else:
            print('server closed')
            s.close()
            break
    except:
        s.close()
        print('exception caught')
        break