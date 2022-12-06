# в целом тот же server.py, что и на предыдущей паре
import os
import socket
import threading

host = '127.0.0.1'
port = 5060

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
messages_ready = []
messages_cards_to_open = []
messages_close = []


def broadcast(message):
    print("broadcast message:", message)
    if 'Ready'.encode('ascii') in messages_ready and len(messages_ready) == 2:
        print('stage 1')
        for client in clients:
            client.send(message)
    elif len(messages_cards_to_open) != 0:
        print('stage 2')
        for client in clients:
            print("send message to client:", client)
            client.send(message)
        messages_cards_to_open.clear()
    elif 'Close'.encode('ascii') in messages_close:
        print('stage 3')
        for client in clients:
            client.send(message)
        messages_close.clear()


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message == 'Ready'.encode('ascii'):
                messages_ready.append(message)
            elif message in [str(i).encode('ascii') for i in range(20)]:
                messages_cards_to_open.append(message)
            elif message == 'Close'.encode('ascii'):
                messages_close.append(message)
            broadcast(message)
        except:
            print('ПОЛЬЗОВАТЕЛЬ ВЫШЕЛ ИЗ ИГРЫ')
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        clients.append(client)
        print(clients)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == '__main__':
    receive()
