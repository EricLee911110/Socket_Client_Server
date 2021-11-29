import socket 
import threading

PORT = 25565
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
accounts = []
file = open('account_data.txt')
listening_max = 10     #Maximum number listening

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET: IPv4, SOCK_STREAM: TCP
server.bind(ADDR) #bind the socket with the address

#Importing the accounts
for x in file:
    account = x.rstrip().split(', ')[0]
    crypted_password = ""
    for x in x.rstrip().split(', ')[1]:
        if x.isupper():
            crypted_password += chr((((ord(x) - 2) -65) %26) +65) #65~90
        elif x.islower():
            crypted_password += chr((((ord(x) -2) -97) %26) +97)  #97~122
        else:
            crypted_password += chr((((ord(x) -2) -48) %10) +48)  #48~57 integer
        
    accounts.append(f"{account}:{crypted_password}")


def SPO(triangle_values, conn, addr):
    converted_triangle_values = list(map(int, triangle_values)) #turn string into int. ['3','4','5'] to [3,4,5]
    converted_triangle_values.sort()  #From min -> max
    a = converted_triangle_values[0]
    b = converted_triangle_values[1]
    c = converted_triangle_values[2]
    if c < a + b:
        if c*c == a*a + b*b: #Right Triangle
            print(f"[{addr}] Triangle side lengths {a}, {b}, {c} form a right triangle.")
            conn.send("Output: Right Triangle".encode(FORMAT))
        elif c*c > a*a + b*b: #Obtuse Triangle
            print(f"[{addr}] Triangle side lengths {a}, {b}, {c} form a obtuse triangle.")
            conn.send("Output: Obtuse Triangle".encode(FORMAT))
        else: #Acute Triangle
            print(f"[{addr}] Triangle side lengths {a}, {b}, {c} form a acute triangle.")
            conn.send("Output: Acute Triangle".encode(FORMAT))
    else: # not a Triangle
        print(f"[{addr}] Triangle side lengths {a}, {b}, {c} is not a triangle.")
        conn.send("Output: Not a Triangle".encode(FORMAT))


def handle_client(conn, addr, client_live):
    verified = False #log in or not
    if client_live > listening_max:
        connected = False
        print("One connection lost.")
        conn.send("server is full".encode(FORMAT))
    else:
        connected = True 
        conn.send("server is ready".encode(FORMAT))

    while connected:
        msg = conn.recv(2048).decode(FORMAT) #2048 represent the size of the buffer, for now it's 2048 bytes
        if verified == True:   #verified account
            if "SPO" in msg:
                triangle_values = msg.split()[0].split(',') #"3,4,5 SPO"
                SPO(triangle_values, conn, addr)    #['3','4','5']
            elif msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr}] Close the TCP socket connection of client {acc_name}")
                conn.send("Output: See ya! Have a nice day!".encode(FORMAT))
            elif "LOGIN" in msg:
                print(f"[{addr}] Client have already log in.")
                conn.send("Output: You have already log in. Try out our SPO command!".encode(FORMAT))
            else:
                print(f"[{addr}] Invalid command.")
                conn.send("Output: Please enter a valid command".encode(FORMAT))
        
        elif verified == False:
            if "LOGIN" in msg:
                if msg.split()[0] in accounts:
                    verified = True
                    acc_name = msg.split(':')[0]
                    print(f"[{addr}] Client '{acc_name}' logins successfully.")
                    conn.send("Output: Valid".encode(FORMAT))
                else:
                    acc_name = msg.split(':')[0]
                    print(f"[{addr}] Client '{acc_name}' is unregistered or enter the incorrect password.")
                    conn.send("Output: Account not registered or incorrect password. Please try again.".encode(FORMAT))
            elif msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr}] One connection lost.")
                conn.send("Output: Sorry. We can't help you without a valid account. Come back next day!".encode(FORMAT))
            elif "SPO" in msg:
                a = msg.split(' ')[0].split(',')[0]
                b = msg.split(' ')[0].split(',')[1]
                c = msg.split(' ')[0].split(',')[2]
                print(f"[{addr}] No permission to process the triangle problem with side lengths of {a}, {b}, and {c}. Please try logging in.")
                conn.send("Output: Permission denied".encode(FORMAT))
            else:
                print(f"[{addr}] Invalid command.")
                conn.send("Output: Permission denied. Try logging in or other command.".encode(FORMAT))
    
    
    conn.close()
        

def start():
    server.listen()
    print("The server is ready to provide service.")
    print(f"The maximum number of connections is {listening_max}.")
    while True:
        conn, addr = server.accept() #accepct the connection from the client #conn: the client socket, addr: the client IP address
        client_live = threading.active_count()
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_live)) #We don't want the other clients waiting, so we create a thread. Each thread can handle one client.
        thread.start() #starting the thread
        print(f"Accept {client_live} connection.") #print out the total connection the server is handling

start()