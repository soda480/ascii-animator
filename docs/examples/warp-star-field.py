import random
from ascii_animator import Animator, Animation, Speed


class WarpStarfield(Animation):
    def __init__(self, width=80, height=24, stars=120):
        self.x_size = width
        self.y_size = height
        self.center_x = width / 2
        self.center_y = height / 2
        self.star_count = stars
        self.palette = ".,:+*#@"
        self.stars = []
        self._grid = []
        self._init_stars()
        self._build_frame()

    @property
    def grid(self):
        return self._grid

    def _init_stars(self):
        self.stars = []
        for _ in range(self.star_count):
            self.stars.append(self._new_star())

    def _new_star(self):
        return {
            "x": random.uniform(-1.0, 1.0),
            "y": random.uniform(-1.0, 1.0),
            "z": random.uniform(0.2, 1.0),
            "pz": None,
        }

    def _empty_grid(self):
        return [[" " for _ in range(self.x_size)] for _ in range(self.y_size)]

    def _project(self, x, y, z):
        scale = 18 / z
        sx = int(self.center_x + x * scale)
        sy = int(self.center_y + y * scale)
        return sx, sy

    def _draw_point(self, grid, x, y, ch):
        if 0 <= x < self.x_size and 0 <= y < self.y_size:
            grid[y][x] = ch

    def _draw_trail(self, grid, x1, y1, x2, y2, ch):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            self._draw_point(grid, x1, y1, ch)
            return

        for i in range(steps + 1):
            x = int(x1 + dx * i / steps)
            y = int(y1 + dy * i / steps)
            self._draw_point(grid, x, y, ch)

    def _brightness_char(self, z):
        index = int((1.0 - z) * (len(self.palette) - 1))
        index = max(0, min(index, len(self.palette) - 1))
        return self.palette[index]

    def _build_frame(self):
        grid = self._empty_grid()

        for star in self.stars:
            star["z"] -= 0.035

            if star["z"] <= 0.03:
                star.update(self._new_star())

            sx, sy = self._project(star["x"], star["y"], star["z"])

            if star["pz"] is None:
                px, py = sx, sy
            else:
                px, py = self._project(star["x"], star["y"], star["pz"])

            ch = self._brightness_char(star["z"])

            self._draw_trail(grid, px, py, sx, sy, ch)
            self._draw_point(grid, sx, sy, "*")

            star["pz"] = star["z"]

            if not (0 <= sx < self.x_size and 0 <= sy < self.y_size):
                star.update(self._new_star())

        cx = int(self.center_x)
        cy = int(self.center_y)
        self._draw_point(grid, cx, cy, "+")

        self._grid = grid

    def cycle(self):
        self._build_frame()
        return False


Animator(
    animation=WarpStarfield(width=100, height=30, stars=140),
    speed=Speed.FAST,
    max_loops=0,
)