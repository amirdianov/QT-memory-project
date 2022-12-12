import socket
import sys

from PyQt6.QtCore import QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget

from backend.handlers import GameWindowHandlers
from frontend.windows import StartWindow, GameWindow, FinishWindow

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONNECTION = ('127.0.0.1', 5060)

CONNECTED = False
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
                        ex2.edit_label(True)
                    elif 'OPPONENT TURN' in message[1]:
                        ex2.queue_turn_false(message[1])
                        ex2.edit_label(False)
                if 'Play' in message:
                    message = message.split('|')
                    # переворот карточек
                    print(f'Хочу перевернуть эту карточку {message[1]}')
                    self.signal.emit(message[1] + '|' + message[-2])
                if 'Close' in message:
                    message = message.split('|')
                    print(message, 'ВОТ ТАК РАЗБИЛОСЬ')
                    if 'YOU TURN' in message[1]:
                        ex2.queue_turn_true(message[1])
                    elif 'OPPONENT TURN' in message[1]:
                        ex2.queue_turn_false(message[1])
                    self.signal.emit('close|' + message[-1])
                if 'is out' in message:
                    player = message[message.find('<'):message.find('>')+1]
                    if str(CLIENT) != player:
                        ex2.go_finish_from_game()
                        ex3.win_window()
                if 'Finish' in message:
                    message = message.split('|')
                    if 'True' in message[1]:
                        ex3.win_window()
                    elif 'False' in message[1]:
                        ex3.lose_window()
            except Exception as exc:
                print(exc)
                print('ОШИБКА')
                break


class MemoryGameStart(StartWindow):
    def __init__(self):
        super().__init__()
        global CONNECTED
        self.client = CLIENT
        if not CONNECTED:
            self.client.connect(CONNECTION)
            CONNECTED = True
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
        if 'close' in message:
            is_mine = message.split('|')[-1] == 'YOU TURN'
            print('hide_cards was called inside update_window method')
            ex2.hide_cards(is_mine=is_mine)
            return
        number, turn = message.split('|')
        if number in [str(i) for i in range(20)]:
            ex2._toggle_card(int(number), turn)

    def open_game(self):
        ex.close()
        ex2.show()
        # window.setCurrentIndex(window.currentIndex() + 1)


class MemoryGame(GameWindow):
    def __init__(self):
        super().__init__()
        self.client = CLIENT
        self.timer.timeout.connect(self.hide_card_double)
        self.back.clicked.connect(self.go_menu_from_game)

    def go_menu_from_game(self):
        self.client.send(f'{self.client} is out'.encode('ascii'))
        ex2.close()
        ex.show()
        # window.setCurrentIndex(window.currentIndex() - 1)

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

    def go_finish_from_game(self):
        super().go_finish_from_game()
        ex2.close()
        ex3.show()
        # window.setCurrentIndex(window.currentIndex() + 1)

    def finish_send(self, message_bool):
        super().finish_send(message_bool)
        print("Вот такое сообщение отправляю", message_bool)
        message = 'Finish|' + message_bool
        print("Вот такое сообщение отправляю", message)
        self.client.send(message.encode('ascii'))


class MemoryGameFinish(FinishWindow):
    def __init__(self):
        super().__init__()
        self.pushButton.clicked.connect(self.go_menu_from_finish)

    def lose_window(self):
        print('lose_window method was called')
        self.setStyleSheet('background-color: rgba(252, 81, 79, 235);')
        self.label.setText('You lose...')
        print('lose_window method was finished')

    def win_window(self):
        print('Я зашел в победу')
        self.setStyleSheet('background-color: rgb(85, 255, 0);')
        self.label.setText('You win!')

    def go_menu_from_finish(self):
        global ex
        ex3.close()
        window.removeWidget(ex)

        ex = MemoryGameStart()
        window.insertWidget(0, ex)
        ex.show()

        # window.setCurrentIndex(window.currentIndex() - 2)


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
