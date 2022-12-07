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
queue_numb = '0'


def broadcast(message):
    global queue_numb
    print("broadcast message:", message)
    if 'Ready'.encode('ascii') in messages_ready and len(messages_ready) == 2:
        print('stage 1')
        print(clients)
        for i in range(len(clients)):
            if i == int(queue_numb):
                clients[i].send(f'READY|YOU TURN'.encode('ascii'))
            else:
                clients[i].send(f'READY|OPPONENT TURN'.encode('ascii'))
        messages_ready.clear()
    elif len(messages_cards_to_open) != 0:
        print('stage 2')
        for i in range(len(clients)):
            print("send message to client:", clients[i])
            if type(message) == bytes:
                message = message.decode('ascii')
            if i == int(queue_numb):
                clients[i].send(f'Play|{message}|YOU TURN'.encode('ascii'))
            else:
                clients[i].send(f'Play|{message}|OPPONENT TURN'.encode('ascii'))
        if len(messages_cards_to_open) == 2:
            messages_cards_to_open.clear()
    elif 'Close'.encode('ascii') in messages_close:
        print('stage 3')
        for client in clients:
            client.send(message)
        # Вот идейно должно работать именно так
        # queue_numb = str(1 - int(queue_numb))
        # for i in range(len(clients)):
        #     if i == int(queue_numb):
        #         clients[i].send(f'Close|YOU TURN'.encode('ascii'))
        #     else:
        #         clients[i].send(f'Close|OPPONENT TURN'.encode('ascii'))
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
        except Exception as ex:
            print(ex)
            print('ПОЛЬЗОВАТЕЛЬ ВЫШЕЛ ИЗ ИГРЫ')
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        clients.append(client)
        print(clients)
        if len(clients) <= 2:
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            print('Увы, вы лишний')


if __name__ == '__main__':
    receive()
