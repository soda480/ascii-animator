import random
from time import sleep
from ascii_animator import Animator, Animation, Speed
from colorama import Style, Fore, Back

class BinarySearch(Animation):

    def __init__(self):
        self.y_size = 7
        self.x_size = 250
        self.reset()

    @property
    def grid(self):
        return self._grid
    
    def cycle(self):
        lo = 0
        item = self._search
        hi = len(self._numbers) - 1
        while True:
            yield self._update_grid(lo, None, hi)
            if self._numbers[lo] == item:
                # return lo
                break
            if self._numbers[hi] == item:
                # return hi
                break
            if hi == lo + 1:
                # return
                break
            md = int((hi + lo) / 2)
            yield self._update_grid(lo, md, hi)
            if self._numbers[md] == item:
                # return md
                break
            elif self._numbers[md] < item:
                lo = md
            else:
                hi = md
        yield self._update_grid(lo, md, hi, done=True)

    def reset(self):
        self._grid = [[' ' for x in range(self.x_size)] for y in range(self.y_size)]
        self._numbers = random.sample(range(1, 75), 30)
        self._numbers.sort()
        self._max_digits = 2
        self._search = random.randrange(75) # self._numbers[-2]

    def _show_numbers(self, items):
        line = [str(number).rjust(self._max_digits, '0') for number in self._numbers]
        for index, style in items:
            if index is None:
                continue
            line[index] = style + line[index] + Style.RESET_ALL
        return ' ' + ' '.join(line)

    def _show_line(self, items):
        length = len(self._numbers)
        pad = self._max_digits * ' '
        line = [pad for _ in range(length)]
        for index, label, style in items:
            if index is None:
                continue
            if isinstance(label, int):
                label = str(label)
            label = label.ljust(self._max_digits, ' ')
            line[index] = style + label + Style.RESET_ALL
        return ' ' + ' '.join(line)

    def _update_grid(self, lo, md, hi, done=False):
        bright_yellow = Style.BRIGHT + Fore.YELLOW
        self._grid[0] = f' Searching for:{self._search}'
        self._grid[1] = self._show_numbers([(md, Style.BRIGHT + Back.YELLOW + Fore.BLACK)])
        self._grid[2] = self._show_line([(lo, u'\u25B2', bright_yellow), (md, u'\u25B2', bright_yellow), (hi, u'\u25B2', bright_yellow)])
        self._grid[3] = self._show_line([(lo, lo, bright_yellow), (md, md, bright_yellow), (hi, hi, bright_yellow)])
        self._grid[4] = self._show_line([(lo, 'lo', bright_yellow), (md, 'md', bright_yellow), (hi, 'hi', bright_yellow)])
        return done


if __name__ == '__main__':
    Animator(animation=BinarySearch(), speed=Speed.VERY_SLOW, max_loops=2)