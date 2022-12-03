import os
from random import shuffle
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

FRUITS: list[str] = [img for img in os.listdir(os.path.join('images')) if img != 'fruits.png']


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

        # for i in range(1, len(self.cards) + 1):
        #     print('i=', i)
        #     setattr(self, f'toggle_card{i}', lambda: self._toggle_card(card_num=i))

    def _handle_player_turn(self, img: str):
        for num in self.is_chosen:
            card_button: QPushButton = getattr(self, f'pushButton_{num}', None)
            card_button.setIcon(QIcon(os.path.join('images', img)))
        self.is_chosen.clear()

    def hide_cards(self):
        self.timer.stop()
        self._handle_player_turn('fruits.png')

    def remove_cards(self):
        self._handle_player_turn('')

    def _toggle_card(self, card_num: int):
        print(card_num)
        print(f'pushButton_{card_num}')
        card_button: QPushButton = getattr(self, f'pushButton_{card_num}', None)
        clicked_count: int = self.is_toggled.count(False)
        print('clicked_count:', clicked_count)
        card_num -= 1
        if clicked_count < 2 and self.is_toggled[card_num]:
            card_button.setIcon(QIcon(os.path.join('images', self.cards[card_num])))
            if (len(self.is_chosen) and self.is_chosen[0] != card_num + 1) or len(self.is_chosen) == 0:
                self.is_chosen.append(card_num + 1)
                print(self.is_chosen)
            if clicked_count == 1:
                if self.cards[self.is_chosen[0]] == self.cards[self.is_chosen[1]]:
                    self.remove_cards()
                else:
                    self.timer.start(1000)
        if clicked_count < 2:
            self.is_toggled[card_num] = not self.is_toggled[card_num]

    # def change_image(self):
    #     print('тут')
    #     if self.is_toggled:
    #         self.pushButton_14.setIcon(QIcon(os.path.join('images', 'apple.png')))
    #         self.timer.start(1000)
    #     else:
    #         self.pushButton_14.setIcon(QIcon(os.path.join('images', 'fruits.png')))
    #     self.is_toggled = not self.is_toggled
    #
    # def hide_image(self):
    #     self.timer.stop()
    #     self.pushButton_14.click()
