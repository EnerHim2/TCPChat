import socket
import threading

ip = input("Server IP: ")
port = input("Server Port: ")
nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, int(port)))

def recieve():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred!\n\n {str(e)}")
            client.close()
            break

def write():
    while True:
        message = nickname + "> " + input("")
        client.send(message.encode("ascii"))

rcv_t = threading.Thread(target=recieve)
rcv_t.start()

wr_t = threading.Thread(target=write)
wr_t.start()