from machine import Pin, I2C
from umenu import *
import ssd1306

i2c = I2C(1, scl=Pin(4), sda=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


class FileList(CustomItem):

    def __init__(self, name):
        super().__init__(name)
        self._menu = None

    def prepare_list(self):
        import os
        files = os.listdir()
        self._menu = Menu(self.display, 5, 10)
        builder = MenuScreen('Files', self.parent)
        for file in files:
            builder.add(FilePreview(file))
        self._menu.set_screen(builder)

    def up(self):
        self._menu.move(-1)

    def down(self):
        self._menu.move()

    def select(self):
        self._menu.click()
        return self

    def draw(self):
        if self._menu is None:
            self.prepare_list()
        self._menu.draw()


class FilePreview(CustomItem):

    def __init__(self,  file):
        super().__init__(file)
        self._file = file

    def select(self):
        return self.parent

    def draw(self):
        f = open(self._file)
        d = f.read()
        self.display.fill(0)
        # this should be adjusted to print few lines only and be sure it match to screen
        # here can be implemented up / down methods to scroll up and down text
        max_l = int(self.display.width / 8)  # standard font width is 8
        chunks = [d[i:i + max_l] for i in range(0, len(d), max_l)]
        y = 0
        for _ in chunks:
            self.display.text(_, 0, y, 1)
            y += 9
        self.display.show()


menu = Menu(display, 4, 12)
menu.set_screen(MenuScreen('Main Menu').add(FileList('Show files')))
menu.draw()
