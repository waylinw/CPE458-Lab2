import socket

TCP_IP = 'localhost'
TCP_PORT = 12345
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while True:
    message = input("Enter input: ")
    if message == 'q':
        break;
    s.send(message.encode())
    data = s.recv(len(message))
    if len(data) is len(message):
        print("received from server: ", data.decode())
    else:
        print("server error")
        s.close()
        break

print('closing connection')
s.close()
print('connection closed')