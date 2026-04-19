from ascii_animator import Animator, Animation, Speed

class Bouncer(Animation):
    def __init__(self, width=20):
        self.y_size = 1
        self.x_size = width
        self.position = 0
        self.direction = 1
        self._grid = [[" " for _ in range(self.x_size)]]
        self._draw()

    @property
    def grid(self):
        return self._grid

    def _draw(self):
        self._grid[0] = [" " for _ in range(self.x_size)]
        self._grid[0][self.position] = "●"

    def cycle(self):
        if self.position == self.x_size - 1:
            self.direction = -1
        elif self.position == 0:
            self.direction = 1
        self.position += self.direction
        self._draw()
        return self.position == 0

Animator(
    animation=Bouncer(),
    speed=Speed.NORMAL,
    max_loops=3)