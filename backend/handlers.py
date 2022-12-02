from PyQt6.QtGui import QIcon
import time


class GameWindowHandlers:
    is_toggled = True

    def change_image(self, checked):
        print(checked)
        print('тут')
        if self.is_toggled:
            self.pushButton_14.setIcon(QIcon(r'images\apple.png'))
        else:
            self.pushButton_14.setIcon(QIcon(r'images\fruits.png'))
        self.is_toggled = not self.is_toggled

    def hide_image(self):
        time.sleep(1)
        self.pushButton_14.click()
