import socket
import random
import sys
from struct import *

option_code = {'GET':1, 'POST':2, 'PUT':3, 'DELETE':4}
msg_type = {'CON':0, 'NONCON':1, 'ACK':2, 'RST':3}

def init():
    UDP_IP = 'localhost'
    UDP_PORT = 12345
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (UDP_IP, UDP_PORT)
    return s, server_address

def parseArguments():
    if len(sys.argv) != 4:
        print("not enough arg: <TYPE> <REQUEST TYPE> <OPTION>")
        exit()
    try:
        req_type = msg_type.get(sys.argv[1])
        assert(req_type != None)
        msg_id = random.randint(1, 1 << 16)
        request_type = option_code.get(sys.argv[2])
        assert(request_type != None)
        request_option = sys.argv[3]
    except:
        print("argument error")
        exit()
    return req_type, msg_id, request_type, request_option

def packMsg(args):
    version = 1 # 2 bit unsigned int
    type = args[0] # 2 bit unsigned int
    option_count = 1 # 4 bit unsigned int
    code = args[2] # 8 bit unsigned int
    message_ID = args[1] # 16bit unsigned int in network byte order
    option_delta = 0 # 4 bit unsigned int
    option_length = len(args[3]) # 4 bit unsigned int
    option_data = args[3] # length must be the length of this, btwn 0 - 16 bytes

    header = (((((((version << 2) | type) << 4) | option_count) << 8) | code) << 16) | message_ID
    options = ((option_delta << 4) | option_length)

    return pack('!IB', header, options) + bytes(option_data, 'utf+8')

# sends data over udp
def sendData(msg, s, server_address):
    try:
        sent = s.sendto(msg, server_address)
    except:
        s.close()
        print('Cannot send data to server')
        exit()

def recvData(s, server_address):
    pass

# def receiveData(s, server_address):
#     while True:
#         try:
#             message = input("Enter input: ")
#             sent = s.sendto(message.encode(), server_address)
#
#             print('waiting for server to respond')
#             data, server = s.recvfrom(1280)
#             if data:
#                 print('received: ', data.decode())
#             else:
#                 print('server closed')
#                 s.close()
#                 break
#         except:
#             s.close()
#             print('exception caught')
#             break


socket, addr = init()

args = parseArguments()
msgToSend = packMsg(args)

sendData(msgToSend, socket, addr)

recvData(socket, addr)
