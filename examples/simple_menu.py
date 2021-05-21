from machine import Pin, I2C
import random
from umenu import *
import ssd1306

i2c = I2C(1, scl=Pin(4), sda=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

menu = Menu(display, 4, 12)
menu.set_screen(MenuScreen('Main Menu')
                .add(ValueItem('Speed', 10, 1, 100, 1, print))
                .add(EnumItem("Mode", ['Option 1', 'Option 2'], print, 0))
                .add(ConfirmItem("Print XXX", (print, 'XXX'), "Do you wanna do that?", ('yeah, sure!', 'nah, sorry!')))
                .add(InfoItem("Mode", visible=lambda: 1 == random.randint(0, 1)))
                )
menu.draw()
