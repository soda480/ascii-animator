import random
from ascii_animator import Animator, Animation, Speed
from colorama import Style, Fore

CHAR = chr(9475)

class SelectionSort(Animation):

    def __init__(self):
        self.y_size = 32
        self.x_size = 120
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
        self._grid = [['' for x in range(self.x_size)] for y in range(self.y_size)]
        # even numbers work better for this animation
        self._numbers = [random.randrange(2, 60, 2) for _ in range(90)]
        # track y position from where bars start - leave two lines for labels
        self._y_pos = self.y_size - 3
        self._show_bars()

    def _update_grid(self, idxi, idxj, idxm, done=False):   
        self._show_bars(idxi=idxi, idxm=idxm)
        self._show_labels(idxi, idxm, done=done)
        return done

    def _get_label(self, items, done=False):
        line = [' ' for _ in range(len(self._numbers))]
        if not done:
            for index, label in items:
                line[index] = Style.BRIGHT + Fore.BLUE + label
        return line

    def _show_labels(self, idxi, idxm, done=False):
        self._grid[self.y_size - 1] = self._get_label([(idxi, 'i'), (idxm, 'm')], done=done)
        self._grid[self.y_size - 2] = self._get_label([(idxi, u'\u25B2'), (idxm, u'\u25B2')], done=done)

    def _get_line(self, y, heights, idxi=None, idxm=None):
        line = []
        for height in heights:
            if y <= self._y_pos - height:
                # height does not reach
                line.append(' ')
            else:
                line.append(CHAR)
        if idxi and idxi != len(heights) - 1:
            # end green highlight
            line[idxi] = Style.RESET_ALL + line[idxi]
        if idxm and idxm != len(heights) - 1:
            # highlight middle
            line[idxm] = Style.BRIGHT + Fore.YELLOW + line[idxm] + Style.RESET_ALL
        return Style.BRIGHT + Fore.GREEN + ''.join(line)

    def _show_bars(self, idxi=None, idxm=None):
        # get heights of all numbers as they relate to the grid
        heights = [int(number / 2) for number in self._numbers]
        for y in range(self._y_pos + 1):
            self._grid[y] = self._get_line(y, heights, idxi=idxi, idxm=idxm)

if __name__ == '__main__':
    Animator(animation=SelectionSort(), speed=Speed.SLOW, max_loops=1)