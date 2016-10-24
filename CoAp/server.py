import socket
import sys
from struct import *
import os
from time import gmtime, strftime

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 12345)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

success_ret_code = {'Created':0x00410000, 'Deleted':0x00420000, 'Valid':0x00430000, 'Changed':0x00440000, 'Content':0x00450000}
client_error_code = {'Bad Request':0x00800000, 'Unauthorized':0x00810000, 'Bad Option':0x00820000, 'Forbidden':0x00830000,
                     'Not Found':0x00840000, 'Method Not Allowed':0x00850000, 'Not Acceptable':0x00860000,
                     'Precondition Failed':0x008C0000, 'Request Entity Too Large':0x008D0000,
                     'Unsupported Content-Format':0x008F0000}
server_error_code = {0x00:'Internal Server Error', 0x01:'Not Implemented', 0x02:'Bad Gateway',
                     0x03:'Service Unavailable', 0x04:'Gateway Timeout', 0x05:'Proxying Not Supported'}

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def GET(header, option_data):
    print("GET Request")

    if find(option_data.decode() + '.html', os.getcwd()):
        code = success_ret_code['Content']

        with open(option_data.decode() + '.html', 'r') as myfile:
            ret_option_data = myfile.read()
    else:
        code = success_ret_code['Not Found']
        ret_option_data = 'Not Found'

    return code, ret_option_data

def POST(header, option_data):
    print("POST Request")

    code = success_ret_code['Created']
    filename = strftime("%H%M%S%d%m%Y", gmtime()) + '.html'
    with open( filename, 'w') as myfile:
        myfile.write(option_data)

    return code, os.getcwd() + '/' + filename

def PUT(header, option_data):
    print("PUT Request")
    return 0

def DELETE(header, option_data):
    print("DELETE Request")

    if find(option_data.decode() + '.html', os.getcwd()):
        code = success_ret_code['Deleted']
        os.remove(os.getcwd() + option_data.decode() + '.html')
        ret_option_data = 'Deleted'
    else:
        code = success_ret_code['Not Found']
        ret_option_data = 'Not Found'

    return code, ret_option_data

options = {1: GET, 2: POST, 3: PUT, 4: DELETE}

def handleReq(header, option_data):
    code = (header[0] & 0x00FF0000) >> 16
    return options[code](header, option_data)

def unpackMsg(data):
    size = calcsize('!IB')
    return unpack('!IB', data[:size]), data[size:]

def packMsg(header, ret_code, ret_msg):
    return pack('!IB', (header[0] | ret_code), header[1]) + bytes(ret_msg, 'utf+8')

def recvData():
    while True:
        print ('waiting for msg')
        data, address = sock.recvfrom(1280)
        print ('received %s bytes from %s' % (len(data), address))
        return data, address

def sendData(data, address):
    sent = sock.sendto(data, address)
    print('sent %s bytes back to %s' % (sent, address))

data, address = recvData()

header_option, option_data = unpackMsg(data)

return_header, return_msg = handleReq(header_option, option_data)

sendData(packMsg(header_option, return_header, return_msg), address)