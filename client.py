import socket
import sys

from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget

from backend.handlers import GameWindowHandlers
from frontend.windows import StartWindow, GameWindow, FinishWindow

# from server import clients

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONNECTION = ('127.0.0.1', 5060)


# def clients_mas(mas):
#     global CLIENTS
#     CLIENTS = parse(mas)


def parse(x) -> list[int]:
    x = x[1:-1]
    x = x.split('>, <')
    # print(x)
    x[0] += '>'
    x[1] = '<' + x[1]
    return x


class ReceiverThread(QThread):
    signal: pyqtSignal = pyqtSignal(str)

    def __init__(self):
        super(ReceiverThread, self).__init__()

    def run(self) -> None:
        while True:
            try:
                message = CLIENT.recv(4096).decode('ascii')
                print('message:', message)
                if 'READY' in message:
                    message = message.split('|')
                    ex.open_game()
                    print('ВЫВОД СООБЩЕНИЯ О ГОТОВНОСТИ К ИГРЕ', message)
                    if 'YOU TURN' in message[1]:
                        ex2.queue_turn_true(message[1])
                    elif 'OPPONENT TURN' in message[1]:
                        ex2.queue_turn_false(message[1])
                if 'Play' in message:
                    message = message.split('|')
                    # переворот карточек
                    print(f'Хочу перевернуть эту карточку {message[1]}')
                    self.signal.emit(message[1] + '|' + message[-2])
                # if message == 'Close':
                #     self.signal.emit('close')
                # Идейно должно работать вот так
                if 'Close' in message:
                    message = message.split('|')
                    print(message, 'ВОТ ТАК РАЗБИЛОСЬ')
                    if 'YOU TURN' in message[1]:
                        ex2.queue_turn_true(message[1])
                    elif 'OPPONENT TURN' in message[1]:
                        ex2.queue_turn_false(message[1])
                    self.signal.emit('close')
                    #     ex2.hide_cards()
            except Exception as exc:
                print(exc)
                print('ОШИБКА')
                break


class MemoryGameStart(StartWindow):
    def __init__(self):
        super().__init__()
        self.client = CLIENT
        self.client.connect(CONNECTION)
        self.start.clicked.connect(self.ready_start_game)

    def ready_start_game(self):
        message = 'Ready'
        self.start.setEnabled(False)
        self.start.setText('Waiting...')
        self.client.send(message.encode('ascii'))
        self.receive_thread = ReceiverThread()
        self.receive_thread.start()
        self.receive_thread.signal.connect(self.update_window)

    def update_window(self, message: str) -> None:
        print('!!!!updated!!!!')
        print('message;', message)
        if message == 'close':
            ex2.hide_cards()
            return
        number, turn = message.split('|')
        if number in [str(i) for i in range(20)]:
            ex2._toggle_card(int(number), turn)


    def open_game(self):
        window.setCurrentIndex(window.currentIndex() + 1)


class MemoryGame(GameWindow):
    def __init__(self):
        super().__init__()
        self.client = CLIENT
        self.timer.timeout.connect(self.hide_card_double)
        self.back.clicked.connect(self.go_menu_from_game)

    def go_menu_from_game(self):
        window.setCurrentIndex(window.currentIndex() - 1)

    def open_card_number(self, num_card):
        super().open_card_number(num_card)
        print('Открываю')
        self.client.send(str(num_card).encode('ascii'))

    def hide_card_double(self):
        print('Закрываю')
        message = 'Close'
        self.client.send(message.encode('ascii'))

    def queue_turn_false(self, message: str) -> None:
        print('Я тут')
        for i in range(1, len(GameWindowHandlers.cards) + 1):
            getattr(self, f'pushButton_{i}', None).setEnabled(False)

    def queue_turn_true(self, message: str) -> None:
        print('Я тут')
        for i in range(1, len(GameWindowHandlers.cards) + 1):
            getattr(self, f'pushButton_{i}', None).setEnabled(True)


class MemoryGameFinish(FinishWindow):
    def __init__(self):
        super().__init__()


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
