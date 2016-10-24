import socket
import random
import sys
from struct import *
from enum import Enum

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
    msg_num = args[1] # 16bit unsigned int in network byte order
    option_delta = 0 # 4 bit unsigned int
    option_length = len(args[3]) # 4 bit unsigned int
    option_data = args[3] # length must be the length of this, btwn 0 - 16 bytes

    header = (((((((version << 2) | type) << 4) | option_count) << 8) | code) << 16) | msg_num
    options = ((option_delta << 4) | option_length)

    return pack('!IB', header, options) + bytes(option_data, 'utf+8')


def sendData(msg, s, server_address):
    try:
        print('sending data')
        sent = s.sendto(msg, server_address)
    except:
        print('Cannot send data to server')

success_ret_code = {0x01:'Created', 0x02:'Deleted', 0x03:'Valid', 0x04:'Changed', 0x05:'Content'}
client_error_code = {0x00:'Bad Request', 0x01:'Unauthorized', 0x02:'Bad Option', 0x03:'Forbidden',
                     0x04:'Not Found', 0x05:'Method Not Allowed', 0x06:'Not Acceptable',
                     0x0C:'Precondition Failed', 0x0D:'Request Entity Too Large', 0x0F:'Unsupported Content-Format'}
server_error_code = {0x00:'Internal Server Error', 0x01:'Not Implemented', 0x02:'Bad Gateway',
                     0x03:'Service Unavailable', 0x04:'Gateway Timeout', 0x05:'Proxying Not Supported'}

ret_code_class = {2:success_ret_code, 4:client_error_code, 5:server_error_code}
ret_code_class_name = {2:'Success', 4:'Client Error', 5:'Server Error'}


def parseReceivedData(data):
    size = calcsize('!I')
    header = unpack('!I', data[:size])
    payload = data[size:]

    code = (header[0] & 0x00FF0000) >> 16

    ret_code = code >> 5
    try:
        status = ret_code_class[ret_code].get(code & 0x1F)
    except KeyError:
        print('Server returned unknown code, retying')
        return 0

    print("Return Code: %s\nDetail: %s" % (ret_code_class_name.get(ret_code), status))

    # if we got a success message, just return the payload
    if ret_code_class[ret_code] == success_ret_code:
        return payload.decode()
    # now we only retry if it's specific server side error
    elif status is server_error_code.get(0x03) or status is server_error_code.get(0x04):
        return 0
    return 1


def recvData(s, server_address):
    print('waiting for server to respond, 2 second timeout')
    s.settimeout(2)
    try:
        data, server = s.recvfrom(1280)
    except:
        data = 0

    if data != 0:
        return parseReceivedData(data)

    return data


socket, addr = init()
args = parseArguments()
msgToSend = packMsg(args)
retry = 4
data_received = 0
while retry > 0 and data_received == 0:
    sendData(msgToSend, socket, addr)
    data_received = recvData(socket, addr)
    retry -= 1

if data_received == 0:
    print('server unreachable after 4 retrys')
elif data_received == 1:
    print('Error has occured, not retrying')
else:
    print('Begin Data:\n%s' % data_received)

socket.close()
