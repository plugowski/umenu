from machine import Pin, I2C
from rotary.rotary_irq import RotaryIRQ  # used https://github.com/miketeachman/micropython-rotary
import ssd1306
import time
import uasyncio as asyncio
from umenu import *

i2c = I2C(1, scl=Pin(4), sda=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


class WifiActions(CustomItem):

    def __init__(self, name, display):
        super().__init__(name)
        self.status = False
        self.display = display

    def select(self):
        return self.parent

    def draw(self):
        self.display.fill(0)
        self.display.rect(0, 0, self.display.width, self.display.height, 1)
        self._centered_text('WIFI: active', 20, 1)
        self._centered_text('225.10.110.30', 34, 1)
        self.display.show()

    def get_status(self):
        return self.status

    def activate(self):
        self.status = not self.status
        self.get_status()

    def _centered_text(self, text, y, c):
        x = int(self.display.width/2 - len(text)*8/2)
        self.display.text(text, x, y, c)


class Config(CustomItem):

    def __init__(self, name):
        super().__init__(name)
        self.statuses = {}

    def get_status(self, *args):
        try:
            return self.statuses[args[0]]
        except KeyError:
            self.statuses[args[0]] = False
            return False

    def toggle(self, *args):
        self.statuses[args[0]] = not self.statuses[args[0]]
        self.get_status(*args)


wifi = WifiActions('WiFi', display)
config = Config('Config')
menu = Menu(display, 4, 12)
menu.set_screen(MenuScreen('Main Menu')
                .add(SubMenuItem('WiFi')
                     .add(WifiActions('Info', display))
                     .add(ToggleItem('Activate', wifi.get_status, wifi.activate)))
                .add(SubMenuItem('Lights')
                     .add(ToggleItem('Headlight', (config.get_status, 1), (config.toggle, 1)))
                     .add(ToggleItem('Backlight', (config.get_status, 2), (config.toggle, 2)))
                     .add(SubMenuItem('LEDs')
                          .add(ToggleItem('Turn ON', (config.get_status, 3), (config.toggle, 3)))))
                .add(SubMenuItem('Main Info')
                     .add(InfoItem('Status:', 'ok'))
                     .add(InfoItem('Temp:', '45.1')))
                )

menu.draw()

sw = Pin(17, Pin.IN, Pin.PULL_UP)


def menu_click(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        menu.click()


sw.irq(menu_click, Pin.IRQ_FALLING)


async def rotary():
    r = RotaryIRQ(19, 21, reverse=True)

    val_old = r.value()
    while True:
        val_new = r.value()
        if val_old != val_new:
            menu.move(-1 if val_old > val_new else 1)
            val_old = val_new
        asyncio.sleep_ms(50)


asyncio.run(rotary())
