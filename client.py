import socket
import sys
import threading

from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget
from frontend.windows import StartWindow, GameWindow, FinishWindow

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONNECTION = ('127.0.0.1', 5060)


def receive():
    while True:
        try:
            message = CLIENT.recv(1024).decode('ascii')
            print(message)
            if message in [str(i) for i in range(20)]:
                print('Принял')
                ex2._toggle_card(int(message))
            print('Прошел первый иф')
            if message == 'Ready':
                print('Зашел во второй')
                ex.open_game()
            print('Вышел из втрого')
            if message == 'Close':
                ex2.hide_cards()
        except:
            print('ОШИБКА')
            break


class MemoryGameStart(StartWindow):
    def __init__(self):
        super().__init__()
        self.client = CLIENT
        self.client.connect(CONNECTION)
        self.start.clicked.connect(self.ready_start_game)

    # def receive(self):
    #     while True:
    #         try:
    #             message = self.client.recv(1024).decode('ascii')
    #             print(message, 'Принимаю')
    #             if message == 'Ready':
    #                 self.open_game()
    #             if message in [str(i) for i in range(20)]:
    #                 print('Принял')
    #                 ex2._toggle_card(int(message))
    #         except:
    #             print('ОШИБКА')
    #             break

    def ready_start_game(self):
        message = 'Ready'
        self.start.setEnabled(False)
        self.start.setText('Waiting...')
        self.client.send(message.encode('ascii'))
        self.receive_thread = threading.Thread(target=receive)
        self.receive_thread.start()

    def open_game(self):
        window.setCurrentIndex(window.currentIndex() + 1)
        # self.game = MemoryGame()
        # print('выполнил инит')
        # # self.close()
        # print('закрыл')
        # self.game.show()


class MemoryGame(GameWindow):
    def __init__(self):
        super().__init__()
        self.client = CLIENT
        self.timer.timeout.connect(self.hide_card_double)

    # def receive_new(self):
    #     while True:
    #         try:
    #             message = self.client.recv(1024).decode('ascii')
    #             print('Я готов принять нажатие на кнопку', int(message))
    #             if int(message) in [i for i in range(20)]:
    #                 print('Принял')
    #                 self._toggle_card(int(message))
    #         except:
    #             # в случае любой ошибки лочим открытые инпуты и выводим ошибку
    #             print('ОШИБКА')
    #             break

    def open_card_number(self, num_card):
        super().open_card_number(num_card)
        print('Открываю')
        self.client.send(str(num_card).encode('ascii'))
        # self.receive_thread = threading.Thread(target=self.receive_new)
        # self.receive_thread.start()

    def hide_card_double(self):
        print('Закрываю')
        message = 'Close'
        self.client.send(message.encode('ascii'))


class MemoryGameFinish(FinishWindow):
    def __init__(self):
        super().__init__()
        self.client = CLIENT


if __name__ == '__main__':
    app = QApplication([])
    ex = MemoryGameStart()
    ex2 = MemoryGame()
    ex3 = MemoryGameFinish()
    window = QStackedWidget()
    window.addWidget(ex)
    window.addWidget(ex2)
    window.addWidget(ex3)
    window.show()
    sys.exit(app.exec())
