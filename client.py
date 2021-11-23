import socket

ip = "127.0.0.1"
port = 25566

server = socket.socket()
server.connect((ip, port))
print(server.recv(1024).decode())

server.close()