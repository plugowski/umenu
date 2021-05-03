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

## Menu Items
This package already contains some basic Menu Items objects which can be used to build your menu

### `SubMenuItem`
Creates new sub-menu with list of items

**Arguments (common for all MenuItems):**
- `name` - to define name visible on screen
- `decorator` - decorator is a text or symbol aligned to right side of screen, can be also callable which return proper 
string. Default: `>`
- `visible` - determine if current section should be visible (read more in Visibility section)
### `InfoItem`
Dummy Item, shows only specified text, with no action.

**Arguments:**

See SubMenuItem, default decorator here is empty.

### `CallbackItem`
Item on menu which is able to trigger any callback specified in argument. After callback, parent screen is returned,
but can be disabled by setting return_parent to False.

**Specific Arguments:**

- `callback` - callable to trigger on click on item (more in section Callback)
- `return_parent` - to determine if parent should be returned or not


### `ToggleItem`
Item to handle toggles, like on/off actions. You can specify state, and callback which will be called to change state.
Actually it's extended version of `CallbackItem`

**Specific Arguments:**

- `state_callback` - callback to check current state
- `change_callback` - callback to toggle current state (True/False)

### `EnumItem`
Selected List, here you can define list which will be displayed after click, and on select that element will be 
passed to callback

**Specific Arguments:**
- `items` - list of items, can be also list of dicts {'value': 'xxx', 'name': 'Fance name'}, where `name` will be 
  displayed on screen and `value` passed to callback
- `callback` - callable called after selecting specific position
- `selected` - define which element should be selected (index or dict key)

### `ValueItem`
Widget to adjust values, by incrementing or decrementing by specified amount.

- `value_reader` - callable to read current value as start to adjust
- `min_v` - minimum value for range
- `max_v` - maximum value for range
- `step` - step to  increment / decrement
- `callback` - callback called on every change of value, value will be passed as last argument 

### `CustomItem`
Abstract class to override by custom logic, see example below. Also you can check `ValueItem` implementation
which extends CustomItem.

```python
menu.set_screen(MenuScreen('Main Menu')
    .add(SubMenuItem('WiFi')
        .add(ToggleItem('Activate', wifi.get_status, wifi.activate)))
    .add(SubMenuItem('Lights')
        .add(ToggleItem('Headlight', (config.get_status, 1), (config.toggle, 1)))
        .add(ToggleItem('Backlight', (config.get_status, 2), (config.toggle, 2)))
    .add(SubMenuItem('Main Info')
        .add(InfoItem('Status:', 'ok'))
        .add(InfoItem('Temp:', '45.1')))
)
menu.draw()
```

![Generated Menu](images/main_menu.jpeg?raw=true "Menu")

## Callbacks

In all MenuItems callbacks can be single callable if no parameters should be passed, or tuple where wirst element is 
callable, and second is a single arg or tuple with `*args`. For example:

```python
CallbackItem('Print it!', (print, 'hello there'))
# will print: hello there
```

```python
CallbackItem('Print it!', (print, (1, 2, 3)))
# will print: 1 2 3
```

## Visibility

Every item can be hidden separately by setting named argument `visible` to False or
by passing callable to 

## CustomItem

To create your own menu logic, you can extend abstract class CustomItem class and implement at least `draw()` and 
`select()` function.

draw() is called once you select specific menu, and selec() is collect when someone click inside CustomItem.

Example usage of some Config class which keeps values in memory:

```python
class Config(CustomItem):

    def __init__(self, name):
        super().__init__(name)
        self.statuses = {}

    def get_status(self, num):
        try:
            return self.statuses[num]
        except KeyError:
            self.statuses[num] = False
            return False

    def toggle(self, num):
        self.statuses[num] = not self.statuses[num]


menu.add_screen(MenuScreen('Main Menu')
    .add(ToggleItem('Config 1', (config.get_status, 1), (config.toggle, 1)))
    .add(ToggleItem('Config 2', (config.get_status, 2), (config.toggle, 2)))
)
```

See [`examples/rotary_encoder_menu.py`](./examples/rotary_encoder_menu.py). 


## License

Copyright (C) 2021, Paweł Ługowski

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.