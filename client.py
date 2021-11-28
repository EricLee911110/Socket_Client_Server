import socket

PORT = 25565
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    if ((".txt" in msg) and ("SPO" in msg)):
        fname = msg.split()[0]
        f = open(fname)
        for x in f:
            client.send(x.rstrip().encode(FORMAT))
            print(client.recv(2048).decode(FORMAT))
    else:
        message = msg.encode(FORMAT)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))

connected = True
while connected:
    msg = input("Input: ")
    send(msg)
    if msg == DISCONNECT_MESSAGE:
        connected = False 

client.close()