from PyQt6.QtGui import QIcon
import time


class GameWindowHandlers:
    def set_image(self):
        print('нажал')
        self.pushButton_14.setIcon(QIcon('images\banana.png'))
        time.sleep(5)
        self.pushButton_14.setIcon(QIcon('images\kisspng-pear-computer-icons-fruit-pear-5abb968c8ec345.2118909615222432125848.png'))
