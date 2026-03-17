from . import DisplayGraphic, Display, CENTER
import framebuf
import gc


class Dashboard:

    def __init__(self, display: Display, blocks: list = None):
        self._windows = []
        self._display = display
        # definition of display parts like: [(x, y, width, height), [...tuple]]
        self._blocks = blocks if blocks is not None else [(0, 0, display.width, display.height)]

    def _build_layout(self):
        self._windows = []
        for block in self._blocks:
            self._windows.append({
                'x': block[0],
                'y': block[1],
                'width': block[2],
                'height': block[3],
                'buff': framebuf.FrameBuffer(
                    bytearray(block[2] * block[3] * 2),
                    block[2],
                    block[3],
                    self._display.format
                )
            })

    def set_layout(self, blocks: list):
        self._windows = []
        self._blocks = blocks

    def draw_frame(self):
        points = [
            (0, 3), (3, 0), (self._display.width - 4, 0), (self._display.width - 1, 3),
            (self._display.width - 1, self._display.height - 4), (self._display.width - 4, self._display.height - 1),
            (3, self._display.height - 1), (0, self._display.height - 4)
        ]
        for i in range(len(points)):
            j = i + 1 if i != len(points) - 1 else 0
            self._display.line(points[i][0], points[i][1], points[j][0], points[j][1], 1)

    def draw(self):
        self._display.fill(0)

        pos = 0
        for _ in self._windows:
            self._display.blit(_['buff'], _['x'], _['y'])
            pos += 1

        self.draw_frame()
        self._display.hline(3, 32, 122, 1)

        self._display.show()
        del self._windows
        gc.collect()
        self._windows = []

    def __setitem__(self, key, value):
        if not isinstance(value, framebuf.FrameBuffer):
            raise ValueError('FrameBuffer object expected!')

        self._windows[key]['buff'] = value

    def _set_data(self, title, value, module):

        if len(self._windows) == 0:
            self._build_layout()

        fbuf, width, height, graphic = self._get_graphic(self._windows[module])
        fbuf.fill(0)

        graphic.rich_text(title, None, 4, align=CENTER)
        graphic.rich_text(str.upper(str(value)), None, 14, 1, 2, align=CENTER)

        fbuf.vline(width - 1, 3, height - 6, 1)

    @staticmethod
    def _get_graphic(module):
        fbuf = module['buff']
        return fbuf, module['width'], module['height'], DisplayGraphic(module['width'], module['height'], fbuf)
