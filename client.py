import socket
import sys

from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget
from frontend.windows import StartWindow, GameWindow, FinishWindow

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONNECTION = ('127.0.0.1', 5060)


class ReceiverThread(QThread):
    signal: pyqtSignal = pyqtSignal(str)

    def __init__(self):
        super(ReceiverThread, self).__init__()

    def run(self) -> None:
        while True:
            try:
                message = CLIENT.recv(1024).decode('ascii')
                print('message:', message)
                if message in [str(i) for i in range(20)]:
                    print('Принял')
                    self.signal.emit(message)
                    # ex2._toggle_card(int(message))
                print('Прошел первый иф')
                if message == 'Ready':
                    print('Зашел во второй')
                    ex.open_game()
                print('Вышел из второго')
                if message == 'Close':
                    ex2.hide_cards()
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
        print(message)
        if message in [str(i) for i in range(20)]:
            ex2._toggle_card(int(message))

    def open_game(self):
        window.setCurrentIndex(window.currentIndex() + 1)


class MemoryGame(GameWindow):
    def __init__(self):
        super().__init__()
        self.client = CLIENT
        self.timer.timeout.connect(self.hide_card_double)

    def open_card_number(self, num_card):
        super().open_card_number(num_card)
        print('Открываю')
        self.client.send(str(num_card).encode('ascii'))

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
