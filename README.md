# uMenu

Simple MicroPython library to create nested and multifunctional menu with callbacks and custom menu items. 

[![uMenu Example on Video](https://img.youtube.com/vi/TZODmWPMVwM/0.jpg)](https://youtu.be/TZODmWPMVwM)

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

**Specific Arguments:**
- `value_reader` - callable to read current value as start to adjust
- `min_v` - minimum value for range
- `max_v` - maximum value for range
- `step` - step to  increment / decrement
- `callback` - callback called on every change of value, value will be passed as last argument

### `CustomItem`
Abstract class to override by custom logic, see example below. Also you can check `ValueItem` implementation
which extends CustomItem.

### `ToggleItem`
Item to handle toggles, like on/off actions. You can specify state, and callback which will be called to change state.
`ToggleItem` is an extension for `CallbackItem`

**Specific Arguments:**

- `state_callback` - callback to check current state
- `change_callback` - callback to toggle current state (True/False)

### `ConfirmItem`
Implementation of `CallbackItem` with prompt screen before calling custom function. Can be used when we need confirmation for specific action.
If user select "no" option, callback won't be triggered.

**Specific Arguments:**
- `question` - can be None, then question "Are you sure?" will be visible
- `answers` - tuple for `yes` and `no`, it'll simply override default tuple ('yes', 'no')

## Example menu
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
# will print: hello there > like print('hello there')
```

```python
CallbackItem('Print it!', (print, (1, 2, 3)))
# will print: 1 2 3 > like print(*args) where *args are taken from tuple
```

## Visibility

Every item can be hidden separately by setting named argument `visible` to False or
by passing callable to check conditions if element should be vissible. Callable should return True or False.

## CustomItem

To create your own menu logic, you can extend abstract class CustomItem class and implement at least `draw()` and 
`select()` function.

`draw()` is called once you click on specifiv CustomItem position, so basically it can do anything you want, what more
that object has included display, so you can simply draw anything on OLED using driver's methods.

Example usage of CustomItem, to draw some status page:

```python
class DrawCustomScreen(CustomItem):

    def __init__(self, name):
      super().__init__(name)
  
    def select(self):
        return self.parent  # this is needed to go back to previous view when SET button is pushed

    def draw(self):
        self.display.fill(0)
        self.display.rect(0, 0, self.display.width, self.display.height, 1)
        self.display.text('SHOW SOME TEXT', 0, 10, 1)
        self.display.hline(0, 32, self.display.width, 1)
        self.display.show()

menu.add_screen(MenuScreen('Main Menu')
    .add(DrawCustomScreen('Text in frame'))
)
```

See [`examples/rotary_encoder_menu.py`](./examples/rotary_encoder_menu.py). 


## License

Copyright (C) 2021, Paweł Ługowski

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.