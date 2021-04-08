import threading
import socket

host = input("Enter hostname: ")
port = input("Enter port: ")
password = input("Select server password: ")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server started")
server.bind((host, int(port)))
print(f"Bound to address {host}:{port}")
server.listen()
print("Listening..")

client_list = []
nicknames_list = []

def broadcast(message):
    for client in client_list:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client_list.index(client)
            client_list.remove(client)
            client.close()
            nickname = nicknames_list[index]
            broadcast(f"{nickname} left the chat".encode("ascii"))
            nicknames_list.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames_list.append(nickname)
        client_list.append(client)

        print(f"Nickname of client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('ascii'))
        client.send("Connected to the server!".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

recieve()