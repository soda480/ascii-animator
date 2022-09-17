import random
from ascii_animator import Animator, Animation, Speed


CHAR = chr(9475)  # chr(9475)  # chr(9608)  # chr(9679)


class EqAmpLevelBars(Animation):

    def __init__(self, y_size, x_size):
        self.y_size = y_size
        self.x_size = x_size
        self.setup()

    @property
    def grid(self):
        return self._grid

    def setup(self):
        self._grid = [[' ' for x in range(self.x_size)] for y in range(self.y_size)]

    def cycle(self):
        y_mid = int(self.y_size / 2)
        x_mid = int(self.x_size / 2)
        top = y_mid
        for x in range(x_mid, self.x_size):
            number = random.randint(0, top)
            numbers = list(range(y_mid - number, y_mid + number))
            for y in range(self.y_size):
                value = CHAR if y in numbers else ' '
                self.grid[y][x] = value
            if x % 3 == 0:
                # decrease top rand range for every other number
                top -= 1 if top > 0 else 0
        # mirror right side of x-axis to left side
        for x in range(0, x_mid):
            for y in range(self.y_size):
                self.grid[y][x] = self.grid[y][(self.x_size - 1) - x]


def main():
    Animator(animation=EqAmpLevelBars(25, 100), speed=Speed.SLOW)


if __name__ == '__main__':  # pragma: no cover
    main()
