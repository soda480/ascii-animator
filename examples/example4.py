from ascii_animator import Animator, Animation, Speed
import random
from time import sleep


class AnimatedText(Animation):

    def __init__(self, y_size, x_size, text):
        self.y_size = y_size
        self.x_size = x_size
        self.text = text
        self.setup()
        self._text = self._init_text()
        self._box = self._init_box()

    def _init_text(self):
        items = []
        for item in random.sample(list(enumerate(self.text)), len(self.text)):
            index = item[0]
            char = item[1]
            items.append(((3, index + 3), ord(char)))
        return items

    def _init_box(self):
        length = len(self.text)
        box = []
        box.append(((5, length + 4), 9499))  # ┛
        box.append(((4, length + 4), 9475))  # ┃
        box.append(((3, length + 4), 9475))  # ┃
        box.append(((2, length + 4), 9475))  # ┃
        box.append(((1, length + 4), 9491))  # ┓
        for index in range(length + 4, 1, -1):   # ━ 9473
            box.append(((1, index), 9473))      
        box.append(((1, 1), 9487))  # ┏ 9487
        box.append(((2, 1), 9475))  # ┃ 9475
        box.append(((3, 1), 9475))  # ┃ 9475
        box.append(((4, 1), 9475))  # ┃ 9475
        box.append(((5, 1), 9495))  # ┗ 9495
        for index in range(1, length + 4):
            box.append(((5, index), 9473))  # ━ 9473
        return box

    def _update_grid(self, items):
        item = items.pop()
        y_pos = item[0][0]
        x_pos = item[0][1]
        ucode = item[1]
        self._grid[y_pos][x_pos] = chr(ucode)

    @property
    def grid(self):
        return self._grid

    def setup(self):
        self._grid = [[' ' for x in range(self.x_size)] for y in range(self.y_size)]

    def cycle(self):
        if self._text:
            self._update_grid(self._text)
        else:
            if self._box:
                self._update_grid(self._box)
            else:
                return True
def main():
    text = 'Hi there! This is some text to animate.'
    text = 'Author: Emilio Reyes (soda480@gmail.com)'
    Animator(animation=AnimatedText(7, len(text) + 6, text), speed=Speed.FAST, show_axis=False, max_loops=1)


if __name__ == '__main__':  # pragma: no cover
    main()
