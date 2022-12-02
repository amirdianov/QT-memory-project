import sys
# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджет
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QMainWindow
from backend.handlers import *


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/start.ui', self)  # Загружаем дизайн
        self.start.clicked.connect(self.open_game)

    def open_game(self):
        self.game = GameWindow()
        self.close()
        self.game.show()


class GameWindow(QMainWindow, GameWindowHandlers):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/game.ui', self)  # Загружаем дизайн
        self.timer = QTimer(self)
        self.back.clicked.connect(self.go_menu_from_game)
        for i in range(1, len(GameWindowHandlers.cards) + 1):
            print(getattr(self, f'toggle_card{i}'))
            getattr(self, f'pushButton_{i}', None).pressed.connect(getattr(self, f'toggle_card{i}'))
        # self.pushButton_14.pressed.connect(self.change_image)
        # self.timer.timeout.connect(self.hide_image)

    def go_menu_from_game(self):
        self.start = StartWindow()
        self.close()
        self.start.show()


class FinishWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/ending_screen.ui', self)  # Загружаем дизайн

    def go_menu_from_finish(self):
        self.start = StartWindow()
        self.close()
        self.start.show()
