# uMenu

Simple MicroPython library for creating nested and multifunctional menu. 

## Installation

Just copy the `umenu.py` module into your MicroPython board, or just add into root dir, or just in a `/lib` folder. 
It's strongly reccomended to froze it into a MicroPython binary image - just place the file inside the `ports/<board>/modules` folder when building MicroPython from source, then flash to the board as usual. 


## Usage

To build simple menu, you should initialize display first (can be any driver which supports `framebuf`, I use ssd1306).
Then create menu object, specify how many items you want to display on one screen and size of one element.

In my example I knnow that menu looks nice when you use 5 lines and 10px height each or 4 lines and 12px height.

```python
import ssd1306
from machine import Pin, I2C
from umenu import *

i2c = I2C(1, scl=Pin(4), sda=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

menu = Menu(display, 5, 10)
menu.add_screen(MenuScreen('Main Menu'))
menu.draw()
```

Example above will draw empty menu with title `Main Menu` on top.

Library allows you to add nested screens, as also implement your own screens with logic.

### Some already implemented menu items are:
- `SubMenuItem` - Creates new sub-menu with list of items.
- `InfoItem` - Show title and value aligned to right
- `ToggleItem` - requires two callbacks as parameters, one to read current state (True/False), and another to change it, you can also pass `*args`
- `CallcackItem` - can trigger any callback assigned to it, by default return parent, but can be disabled by setting return_parent to False
- `EnumItem` - kind of selectable item, where should be defined list of positions, and selected item will be returned to callback
- `ValueItem` - allows you to adjust specific value using menu buttons/encoder
- `CustomItem` - this class should be overridden by your own logic (more info below)

```python
menu.add_screen(MenuScreen('Main Menu')
    .add(SubMenuItem('WiFi')
        .add(ToggleItem('Activate', wifi.get_status, wifi.activate)))
    .add(SubMenuItem('Lights')
        .add(ToggleItem('Headlight', config.get_status, config.toggle, 1))
        .add(ToggleItem('Backlight', config.get_status, config.toggle, 2))
    .add(SubMenuItem('Main Info')
        .add(InfoItem('Status:', 'ok'))
        .add(InfoItem('Temp:', '45.1')))
)
menu.draw()
```

![Generated Menu](images/main_menu.jpeg?raw=true "Menu")

## CustomItem

To create your own menu logic, you can extend abstract class CustomItem class and implement at least `draw()` and `select()` function.

draw() is called once you select specific menu, and selec() is collect when someone click inside CustomItem.

Example usage of some Config class which keeps values in memory:

```python
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


menu.add_screen(MenuScreen('Main Menu')
    .add(ToggleItem('Config 1', config.get_status, config.toggle, 1))
    .add(ToggleItem('Config 2', config.get_status, config.toggle, 2))
)
```

See [`examples/rotary_encoder_menu.py`](./examples/rotary_encoder_menu.py). 


## License

Copyright (C) 2021, Paweł Ługowski

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.