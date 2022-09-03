import random
from colorama import init as colorama_init
from colorama import Style
from colorama import Fore
from ascii_animator import Animator, Animation, Speed

# CHARS = [chr(c) for c in range(11904, 12019)]
# CHARS = [chr(c) for c in range(9600, 9719)]
CHARS1 = [chr(c) for c in range(10240, 10495)]
CHARS2 = [chr(c) for c in range(9600, 9621)]
CHARS = CHARS1 + CHARS2


class Matrix(Animation):

    def __init__(self, y_size, x_size):
        self.y_size = y_size
        self.x_size = x_size
        colorama_init()
        print(Style.BRIGHT, end='')
        self.setup()
        self._y_count = 1
        self._feed_y_index = 0
        self._setup_feed()
    
    def __del__(self):
        print(Style.RESET_ALL)

    def _setup_feed(self):
        self._feed = []
        total = int(self.x_size / 3)
        for _ in range(total):
            self._feed.append([f'{Fore.GREEN}{random.choice(CHARS)}' for _ in range(self.y_size)])

    @property
    def grid(self):
        return self._grid

    def setup(self):
        self._grid = [[' ' for x in range(self.x_size)] for y in range(self.y_size)]

    def cycle(self):
        for y in range(self.y_size):
            if y not in list(range(self._y_count)):
                # allows for rolling list
                continue
            feed_x_index = 0
            for x in range(self.x_size):
                if x % 5 == 0:
                    # create effect for every 5th column
                    self._grid[y][x] = self._feed[feed_x_index][self._feed_y_index - y]
                    feed_x_index += 1
        self._feed_y_index += 1
        if self._feed_y_index == self.y_size:
            self._feed_y_index = 0
        self._y_count += 1

    def cycle2(self):
        for y in range(self.y_size):
            for x in range(self.x_size):
                self._grid[y][x] = random.choice(CHARS)

def main():
    Animator(animation=Matrix(35, 125), speed=Speed.SLOW)


if __name__ == '__main__':  # pragma: no cover
    main()
