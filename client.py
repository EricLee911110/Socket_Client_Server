import socket
import time

PORT = 25565
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET: IPv4, SOCK_STREAM: TCP
client.connect(ADDR) #connect the client to the server
#The varible for us to know they are still connecting

server_status = client.recv(2048).decode(FORMAT)
if server_status == "server is ready":
    connected = True
elif server_status == "server is full":
    connected = False
    print("The server is busy right now. Please try again later.")

def send(msg):
    if ((".txt" in msg) and ("SPO" in msg)): #One input, but multiple output
        fname = msg.split()[0] #"triangle_data_example.txt SPO"
        f = open(fname)
        for x in f: #send each line in the txt file
            client.send(x.rstrip().encode(FORMAT))
            print(client.recv(2048).decode(FORMAT))
    else:                                    #One input, one output
        message = msg.encode(FORMAT)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))

while connected:
    msg = input("Input: ")
    send(msg)
    if msg == DISCONNECT_MESSAGE:
        connected = False 

client.close()