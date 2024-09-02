import random
from time import sleep
from ascii_animator import Animator, Animation, Speed
from colorama import Style, Fore, Back

class SelectionSort(Animation):

    def __init__(self):
        self.y_size = 7
        self.x_size = 250
        self.reset()

    @property
    def grid(self):
        return self._grid
    
    def cycle(self):
        length = len(self._numbers)
        for idxi in range(length):
            idxm = idxi
            for idxj in range(idxi + 1, length):
                if self._numbers[idxj] < self._numbers[idxm]:
                    idxm = idxj
                # display numbers as they are being sorted
                yield self._update_grid(idxi, idxj, idxm)
            # swap numbers
            self._numbers[idxi], self._numbers[idxm] = self._numbers[idxm], self._numbers[idxi]
        # display numbers after they have been sorted
        yield self._update_grid(idxi, idxj, idxm, done=True)

    def reset(self):
        self._grid = [[' ' for x in range(self.x_size)] for y in range(self.y_size)]
        self._numbers = random.sample(range(1, 75), 30)
        self._max_digits = 2

    def _show_numbers(self, items, done=False):
        line = [str(number).rjust(self._max_digits, '0') for number in self._numbers]
        if not done:
            # check if numbers have not been sorted then proceed with styling
            for index, style in items:
                line[index] = style + line[index] + Style.RESET_ALL
        return ' ' + Style.BRIGHT + Fore.GREEN + ' '.join(line)

    def _show_line(self, items):
        length = len(self._numbers)
        pad = self._max_digits * ' '
        line = [pad for _ in range(length)]
        for index, label, style in items:
            if isinstance(label, int):
                label = str(label)
            line[index] = style + label + Style.RESET_ALL
        return ' ' + ' '.join(line)

    def _update_grid(self, idxi, idxj, idxm, done=False):
        bright_yellow = Style.BRIGHT + Fore.YELLOW
        self._grid[0] = self._show_line([(idxi, 'i', bright_yellow)])
        self._grid[1] = self._show_line([(idxi, idxi, bright_yellow)])
        self._grid[2] = self._show_line([(idxi, u'\u25BC', bright_yellow)])
        self._grid[3] = self._show_numbers([(idxi, Style.RESET_ALL), (idxm, Style.BRIGHT + Back.YELLOW + Fore.BLACK)], done=done)
        self._grid[4] = self._show_line([(idxj, u'\u25B2', bright_yellow)])
        self._grid[5] = self._show_line([(idxj, idxj, bright_yellow)])
        self._grid[6] = self._show_line([(idxj, 'j', bright_yellow)])
        return done


if __name__ == '__main__':
    Animator(animation=SelectionSort(), speed=Speed.FAST, max_loops=1)