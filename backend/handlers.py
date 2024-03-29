import os
import time
from random import shuffle
from socket import socket
from typing import Optional

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QLCDNumber, QApplication

FRUITS: list[str] = [img for img in os.listdir(os.path.join('images')) if img != 'fruits.png' and img != 'images.qrc']


class GameWindowHandlers:
    def __init__(self):
        self.OPENED_CARDS: list[str] = []
        self.cards: list[str] = [*[FRUITS[num] for num in range(9)],
                                 *[FRUITS[num] for num in range(9)]]
        # shuffle(cards)
        self.is_toggled: list[bool] = [True] * 18
        self.is_chosen: list[int] = []


    def toggle_card1(self):
        self.open_card_number(1)

    def toggle_card2(self):
        self.open_card_number(2)

    def toggle_card3(self):
        self.open_card_number(3)

    def toggle_card4(self):
        self.open_card_number(4)

    def toggle_card5(self):
        self.open_card_number(5)

    def toggle_card6(self):
        self.open_card_number(6)

    def toggle_card7(self):
        self.open_card_number(7)

    def toggle_card8(self):
        self.open_card_number(8)

    def toggle_card9(self):
        self.open_card_number(9)

    def toggle_card10(self):
        self.open_card_number(10)

    def toggle_card11(self):
        self.open_card_number(11)

    def toggle_card12(self):
        self.open_card_number(12)

    def toggle_card13(self):
        self.open_card_number(13)

    def toggle_card14(self):
        self.open_card_number(14)

    def toggle_card15(self):
        self.open_card_number(15)

    def toggle_card16(self):
        self.open_card_number(16)

    def toggle_card17(self):
        self.open_card_number(17)

    def toggle_card18(self):
        self.open_card_number(18)

    def open_card_number(self, num_card):
        pass

    def edit_label(self, is_mine: bool):
        label = getattr(self, 'label', None)
        label.setText(('Your' if is_mine else 'Opponent') + ' turn')
        label.setStyleSheet('border: 5px solid rgb(85, 255, 0); border-radius: 10px;' if is_mine else
                            'border: 5px solid rgba(252, 81, 79, 235); border-radius: 10px;')

    def _handle_player_turn(self, img: Optional[str] = None, is_mine: bool = True):
        for num in self.is_chosen:
            card_button: QPushButton = getattr(self, f'pushButton_{num}', None)
            if img is not None:
                card_button.setIcon(QIcon(os.path.join('images', img)))
            else:
                card_button.setStyleSheet('border: 5px solid rgb(85, 255, 0); border-radius: 10px;')
                self.is_toggled[num - 1] = False
        if img is None:
            lcd_number: QLCDNumber = getattr(self, 'lcdNumber' + ('_2' if is_mine else ''), None)
            lcd_number.display(lcd_number.intValue() + 1)
            for num in self.is_chosen:
                card_button: QPushButton = getattr(self, f'pushButton_{num}', None)
                card_button.setStyleSheet('border: 5px solid rgb(85, 255, 0); border-radius: 10px;' if is_mine else
                                          'border: 5px solid rgba(252, 81, 79, 235); border-radius: 10px;')
        self.edit_label(is_mine)
        self.edit_label(is_mine)
        self.is_chosen.clear()

    def hide_cards(self, is_mine=True):
        self.timer.stop()
        self._handle_player_turn('fruits.png', is_mine=is_mine)

    def open_cards(self, is_mine=True):
        self._handle_player_turn(is_mine=is_mine)

    def go_finish_from_game(self):
        pass

    def finish_send(self, message):
        pass

    def _toggle_card(self, card_num: int, turn: str):
        print('_toggle_card was called')
        print(card_num)
        print(f'pushButton_{card_num}')
        card_button: QPushButton = getattr(self, f'pushButton_{card_num}', None)
        clicked_count: int = len(self.is_chosen)
        print('clicked_count:', clicked_count)
        card_num -= 1
        if self.is_toggled[card_num] and clicked_count < 2:
            card_button.setIcon(QIcon(os.path.join('images', self.cards[card_num])))
            if len(self.is_chosen) == 0 or (len(self.is_chosen) and self.is_chosen[0] != card_num + 1):
                self.is_chosen.append(card_num + 1)
                print(self.is_chosen)
            if clicked_count == 1 and len(self.is_chosen) == 2:
                print('is_chosen:', self.is_chosen, self.cards)
                if self.cards[self.is_chosen[0] - 1] == self.cards[self.is_chosen[1] - 1]:
                    is_mine: bool = turn == 'YOU TURN'
                    self.OPENED_CARDS.extend([self.cards[self.is_chosen[0] - 1], self.cards[self.is_chosen[1] - 1]])
                    self.open_cards(is_mine)
                    if len(self.OPENED_CARDS) == 18:
                        lcd_number_mine: QLCDNumber = getattr(self, 'lcdNumber_2', None)
                        lcd_number_opponent: QLCDNumber = getattr(self, 'lcdNumber', None)
                        self.go_finish_from_game()
                        print(lcd_number_mine.value(), 'МОИ ОЧКИ')
                        print(lcd_number_opponent.value(), 'ЕГО ОЧКИ')
                        ans = lcd_number_mine.value() > lcd_number_opponent.value()
                        print(ans)
                        self.finish_send(str(ans))

                else:
                    self.timer.start(1000)
