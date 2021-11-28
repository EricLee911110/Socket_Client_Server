import socket 
import threading

PORT = 25565
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def SPO(triangle_values, conn):
    converted_triangle_values = list(map(int, triangle_values))
    converted_triangle_values.sort()
    a = converted_triangle_values[0]
    b = converted_triangle_values[1]
    c = converted_triangle_values[2]
    if c < a + b:
        if c*c == a*a + b*b:
            conn.send("Right Triangle".encode(FORMAT))
        elif c*c > a*a + b*b:
            conn.send("Obtuse Triangle".encode(FORMAT))
        else:
            conn.send("Acute Triangle".endcode(FORMAT))
    else:
        conn.send("Not a Triangle")


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(2048).decode(FORMAT)    
        if "SPO" in msg:
            triangle_values = msg.split()[0].split(',')
            SPO(triangle_values, conn)    #['3','4','5']
        elif msg == DISCONNECT_MESSAGE:
            connected = False

        print(f"[{addr}] {msg}")
    

    conn.close()
        

def start():
    server.listen(10)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()