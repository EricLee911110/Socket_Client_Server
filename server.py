import socket


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 25566 #1024 ~ 65353
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = IPv4 #SOCK_STREAM = TCP

    server.bind((ip, port))
    server.listen(10)
    print("The server is ready to provide service.")   
    print("The maximum number of connections is 10.")

while True:
    client, address = server.accept()
    print("Got connection from", address)
    client.send("Thank you for connecting".encode()) #encode using UTF-8. #non-ascii code may not be available during some part of the process
    client.close()
    break