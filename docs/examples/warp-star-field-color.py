import math
import random
from ascii_animator import Animator, Animation, Speed


class WarpStarfield(Animation):
    RESET = "\033[0m"

    COLORS = {
        "white": "\033[97m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "yellow": "\033[93m",
    }

    def __init__(self, width=100, height=30, stars=140):
        self.x_size = width
        self.y_size = height
        self.center_x = width // 2
        self.center_y = height // 2
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
        angle = random.uniform(0, math.tau)
        radius = random.uniform(0.02, 1.0) ** 0.5

        return {
            "x": math.cos(angle) * radius,
            "y": math.sin(angle) * radius,
            "z": random.uniform(0.2, 1.0),
            "pz": None,
            "color": self._random_star_color(),
        }

    def _random_star_color(self):
        roll = random.random()

        if roll < 0.72:
            return "white"
        if roll < 0.82:
            return "cyan"
        if roll < 0.90:
            return "blue"
        if roll < 0.96:
            return "yellow"
        return "magenta"

    def _empty_grid(self):
        return [[" " for _ in range(self.x_size)] for _ in range(self.y_size)]

    def _project(self, x, y, z):
        scale = 18 / z
        sx = round(self.center_x + x * scale)
        sy = round(self.center_y + y * scale)
        return sx, sy

    def _draw_point(self, grid, x, y, value):
        if 0 <= x < self.x_size and 0 <= y < self.y_size:
            grid[y][x] = value

    def _draw_trail(self, grid, x1, y1, x2, y2, value):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            self._draw_point(grid, x1, y1, value)
            return

        for i in range(steps + 1):
            x = round(x1 + dx * i / steps)
            y = round(y1 + dy * i / steps)
            self._draw_point(grid, x, y, value)

    def _brightness_char(self, z):
        index = int((1.0 - z) * (len(self.palette) - 1))
        index = max(0, min(index, len(self.palette) - 1))
        return self.palette[index]

    def _colorize(self, ch, color_name):
        return f"{self.COLORS[color_name]}{ch}{self.RESET}"

    def _trail_char(self, z, color_name):
        ch = self._brightness_char(min(1.0, z + 0.20))
        return self._colorize(ch, color_name)

    def _star_char(self, z, color_name):
        if z < 0.18:
            return self._colorize("@", "white")
        if z < 0.30:
            return self._colorize("#", color_name)
        return self._colorize(self._brightness_char(z), color_name)

    def _respawn_star(self, star):
        star.clear()
        star.update(self._new_star())

    def _build_frame(self):
        grid = self._empty_grid()

        for star in self.stars:
            star["z"] -= 0.035

            if star["z"] <= 0.03:
                self._respawn_star(star)
                continue

            sx, sy = self._project(star["x"], star["y"], star["z"])

            if star["pz"] is None:
                px, py = sx, sy
            else:
                px, py = self._project(star["x"], star["y"], star["pz"])

            if not (0 <= sx < self.x_size and 0 <= sy < self.y_size):
                self._respawn_star(star)
                continue

            trail_value = self._trail_char(star["z"], star["color"])
            star_value = self._star_char(star["z"], star["color"])

            self._draw_trail(grid, px, py, sx, sy, trail_value)
            self._draw_point(grid, sx, sy, star_value)

            star["pz"] = star["z"]

        self._draw_point(
            grid,
            self.center_x,
            self.center_y,
            self._colorize("+", "white"),
        )

        self._grid = grid

    def cycle(self):
        self._build_frame()
        return False


Animator(
    animation=WarpStarfield(width=100, height=30, stars=140),
    speed=Speed.FAST,
    max_loops=0,
)