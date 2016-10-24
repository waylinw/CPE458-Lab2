import socket
import sys
from struct import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 12345)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

def GET(header, option_data):
    print("GET Request")
    return 0

def POST(header, option_data):
    print("POST Request")
    return 0

def PUT(header, option_data):
    print("PUT Request")
    return 0

def DELETE(header, option_data):
    print("DELETE Request")
    return 0

options = {1: GET, 2: POST, 3: PUT, 4: DELETE}

def handleReq(header, option_data):
    code = (header[0] & 0x00FF0000) >> 16
    return options[code](header, option_data)

def unpackMsg(data):
    size = calcsize('!IB')
    return unpack('!IB', data[:size]), data[size:]

def packMsg():
    pass

def recvData():
    while True:
        print ('waiting for msg')
        data, address = sock.recvfrom(1280)
        print ('received %s bytes from %s' % (len(data), address))
        header_option, option_data = unpackMsg(data)

        return_msg = handleReq(header_option, option_data)

        if return_msg:
            sent = sock.sendto(return_msg, address)
            print('sent %s bytes back to %s' % (sent, address))

def sendData():
    pass

recvData()