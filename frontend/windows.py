import sys
# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджет
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QMainWindow
from backend.handlers import *


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/start.ui', self)  # Загружаем дизайн


class GameWindow(QMainWindow, GameWindowHandlers):
    def __init__(self):
        super().__init__()
        GameWindowHandlers.__init__(self)
        uic.loadUi('ui_files/game.ui', self)  # Загружаем дизайн
        self.timer = QTimer(self)

        for i in range(1, len(self.cards) + 1):
            print(f'pushButton_{i}')
            getattr(self, f'pushButton_{i}', None).clicked.connect(getattr(self, f'toggle_card{i}'))


class FinishWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/ending_screen.ui', self)  # Загружаем дизайн


