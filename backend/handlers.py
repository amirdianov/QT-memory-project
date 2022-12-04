import os
from random import shuffle
from typing import Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLCDNumber

FRUITS: list[str] = [img for img in os.listdir(os.path.join('images')) if img != 'fruits.png' and img != 'image.qrc']


class GameWindowHandlers:
    cards: list[str] = [*[FRUITS[num] for num in range(9)],
                        *[FRUITS[num] for num in range(9)]]
    # shuffle(cards)
    is_toggled: list[bool] = [True] * 18
    is_chosen: list[int] = []

    def toggle_card1(self):
        return self._toggle_card(1)

    def toggle_card2(self):
        return self._toggle_card(2)

    def toggle_card3(self):
        return self._toggle_card(3)

    def toggle_card4(self):
        return self._toggle_card(4)

    def toggle_card5(self):
        return self._toggle_card(5)

    def toggle_card6(self):
        return self._toggle_card(6)

    def toggle_card7(self):
        return self._toggle_card(7)

    def toggle_card8(self):
        return self._toggle_card(8)

    def toggle_card9(self):
        return self._toggle_card(9)

    def toggle_card10(self):
        return self._toggle_card(10)

    def toggle_card11(self):
        return self._toggle_card(11)

    def toggle_card12(self):
        return self._toggle_card(12)

    def toggle_card13(self):
        return self._toggle_card(13)

    def toggle_card14(self):
        return self._toggle_card(14)

    def toggle_card15(self):
        return self._toggle_card(15)

    def toggle_card16(self):
        return self._toggle_card(16)

    def toggle_card17(self):
        return self._toggle_card(17)

    def toggle_card18(self):
        return self._toggle_card(18)

    def _handle_player_turn(self, img: Optional[str] = None):
        for num in self.is_chosen:
            card_button: QPushButton = getattr(self, f'pushButton_{num}', None)
            if img is not None:
                card_button.setIcon(QIcon(os.path.join('images', img)))
            else:
                card_button.setStyleSheet('border: 5px solid rgb(85, 255, 0); border-radius: 10px;')
                self.is_toggled[num - 1] = False
        if img is None:
            lcd_number: QLCDNumber = getattr(self, f'lcdNumber_2', None)
            lcd_number.display(lcd_number.intValue() + 1)
        self.is_chosen.clear()

    def hide_cards(self):
        self.timer.stop()
        self._handle_player_turn('fruits.png')

    def open_cards(self):
        self._handle_player_turn()

    def _toggle_card(self, card_num: int):
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
            if clicked_count == 1:
                if self.cards[self.is_chosen[0] - 1] == self.cards[self.is_chosen[1] - 1]:
                    self.open_cards()
                else:
                    self.timer.start(1000)
