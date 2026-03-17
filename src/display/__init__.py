import gc
from micropython import const
import framebuf
import sh1106

LEFT = const(0)
CENTER = const(1)
RIGHT = const(2)


class DisplayGraphic:

    def __init__(self, width, height, buff=None, format=framebuf.MONO_VLSB):
        self.width = width
        self.height = height
        self._format = format
        self._buff = buff if buff is not None else framebuf.FrameBuffer(bytearray(width * height), width, height, self._format)

    def text(self, text, x, y, c=1, align=LEFT):
        self._buff.text(text, self._start_text_x(text, x, align), y, c)

    def rich_text(self, text, x, y, color=1, size=1, font=None, align=LEFT):
        _font = font if font is not None else self._get_font_by_size(size)
        x = self._start_text_x(text, x, align, _font.width()) + ((size if align == CENTER else 0) // 2)
        memory = {}

        for char in text:
            if char in memory:
                _char = memory[char]
            else:
                _char = _font.get_char(char)
                if color == 0:
                    for i, v in enumerate(_char):
                        _char[i] = 0xFF & ~v
                memory[char] = _char

            fb = framebuf.FrameBuffer(_char, _font.width(), _font.height(), self._format)
            self._buff.blit(fb, x, y)
            x += _font.width()

        del memory
        del _font  # remove from memory
        gc.collect()

    @staticmethod
    def _get_font_by_size(size):
        if size == 1:
            from .fonts import font_6x7
            return font_6x7
        elif size == 2:
            from .fonts import font_12x14
            return font_12x14
        elif size == 5:
            from .fonts import font_30x35
            return font_30x35

        raise IndexError

    def _start_text_x(self, text, x, align=CENTER, font_width=8, font_size=1):
        if align == CENTER:
            return int(self.width / 2 - len(text) * font_width * font_size / 2)
        elif align == RIGHT:
            return int(self.width - len(text) * font_width * font_size)
        return x


class Display:

    def __init__(self, width, height, driver, format=framebuf.MONO_VLSB):
        self.driver = driver
        self.width = width
        self.height = height
        self.format = format  # framebuf.MVLSB (SH1106) or MONO_VLSB (SSD1306)
        self.graphic = DisplayGraphic(width, height, self.driver, self.format)

    def text(self, text, x, y, c=1, align=None):
        if align is None:
            self.driver.text(text, x, y, c)
        else:
            self.graphic.text(text, x, y, c, align)

    def rich_text(self, text, x, y, color=1, size=1, font=None, align=LEFT):
        self.graphic.rich_text(text, x, y, color, size, font, align)

    def show(self):
        self.driver.show()

    def fill(self):
        self.driver.fill()

    def clear(self):
        self.driver.clear()

    def rectangle(self, x, y, width, height, color=1, size=1, font=None, align=LEFT):
        self.driver.rectangle(x, y, width, height, color, size, font, align)

    def fill_rect(self, x, y, width, height, color=1, size=1, font=None, align=LEFT):
        self.driver.fill_rect(x, y, width, height, color, size, font, align)

    def line(self, x1, y1, x2, y2, color=1, size=1, font=None, align=LEFT):
        self.driver.line(x1, y1, x2, y2, color, size, font, align)

    def circle(self, x1, y1, x2, y2, color=1, size=1, font=None, align=LEFT):
        self.driver.circle(x, y, color, size, font, align)

    def fill_circle(self, x1, y1, x2, y2, color=1, size=1, font=None, align=LEFT):
        self.driver.fill_circle(x, y, color, size, font, align)