from ascii_animator import Animator, Animation, Speed


class CyberWalker(Animation):
    RESET = "\033[0m"

    COLORS = {
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "yellow": "\033[93m",
        "white": "\033[97m",
        "blue": "\033[94m",
    }

    def __init__(self, width=100, height=28):
        self.x_size = width
        self.y_size = height
        self.frame = 0
        self.pos = 0
        self._grid = []
        self._build_frame()

    @property
    def grid(self):
        return self._grid

    def _colorize(self, ch, color):
        return f"{self.COLORS[color]}{ch}{self.RESET}"

    def _empty(self):
        return [[" " for _ in range(self.x_size)] for _ in range(self.y_size)]

    def _draw_point(self, grid, x, y, value):
        if 0 <= x < self.x_size and 0 <= y < self.y_size:
            grid[y][x] = value

    def _draw_text(self, grid, art, x, y, color_map=None):
        for dy, row in enumerate(art):
            for dx, ch in enumerate(row):
                if ch == " ":
                    continue
                color = color_map.get(ch) if color_map else None
                value = self._colorize(ch, color) if color else ch
                self._draw_point(grid, x + dx, y + dy, value)

    def _draw_rain(self, grid):
        for x in range(0, self.x_size, 3):
            y = (self.frame * 2 + x) % self.y_size
            self._draw_point(grid, x, y, self._colorize("|", "blue"))
            if y - 1 >= 0 and (x + self.frame) % 4 == 0:
                self._draw_point(grid, x, y - 1, self._colorize(".", "cyan"))

    def _draw_ground(self, grid, base_y):
        for x in range(self.x_size):
            if (x + self.frame) % 7 == 0:
                ch = "_"
            elif (x + self.frame * 2) % 11 == 0:
                ch = "-"
            else:
                ch = "."
            self._draw_point(grid, x, base_y, self._colorize(ch, "magenta"))

        for x in range(0, self.x_size, 8):
            trail_x = (x - self.frame * 3) % self.x_size
            self._draw_point(grid, trail_x, base_y - 1, self._colorize("=", "cyan"))

    def _walker_frames(self):
        return [
            [
                "  .-^-.   ",
                " /_o o_\\  ",
                "    ^==|  ",
                "   /|\\_   ",
                "  / |  \\_ ",
                "    |     ",
                "   / \\    ",
                " _/   \\   ",
            ],
            [
                "  .-^-.   ",
                " /_o o_\\  ",
                "    ^==|  ",
                "   /|\\_   ",
                "  / |  \\_ ",
                "    |     ",
                "   / \\_   ",
                " _/   \\   ",
            ],
            [
                "  .-^-.   ",
                " /_o o_\\  ",
                "    ^==|  ",
                "   /|\\_   ",
                "  / |  \\_ ",
                "    |     ",
                "  _/ \\    ",
                "    /  \\_ ",
            ],
            [
                "  .-^-.   ",
                " /_o o_\\  ",
                "    ^==|  ",
                "   /|\\_   ",
                " _/ |  \\  ",
                "    |     ",
                "   / \\    ",
                " _/   \\   ",
            ],
        ]

    def _walker_colors(self):
        return {
            ".": "white",
            "-": "white",
            "^": "magenta",
            "o": "yellow",
            "=": "cyan",
            "/": "white",
            "\\": "white",
            "_": "blue",
            "|": "white",
        }

    def _draw_motion_trail(self, grid, x, y, frame_art):
        for offset in (2, 4, 6):
            trail_x = x - offset
            for dy, row in enumerate(frame_art):
                for dx, ch in enumerate(row):
                    if ch == " ":
                        continue
                    if ch in ("o", "="):
                        continue
                    if (dx + dy + offset + self.frame) % 3 == 0:
                        self._draw_point(grid, trail_x + dx, y + dy, self._colorize(".", "blue"))

    def _draw_neon_signs(self, grid):
        signs = [
            (8, 3, "N E O N", "cyan"),
            (self.x_size - 18, 6, "VOID", "magenta"),
            (self.x_size // 2 - 5, 2, "404", "yellow"),
        ]

        for sx, sy, text, color in signs:
            for i, ch in enumerate(text):
                if ch != " ":
                    self._draw_point(grid, sx + i, sy, self._colorize(ch, color))

    def _build_frame(self):
        grid = self._empty()
        base_y = self.y_size - 3

        self._draw_rain(grid)
        self._draw_neon_signs(grid)
        self._draw_ground(grid, base_y)

        frames = self._walker_frames()
        art = frames[self.frame % len(frames)]
        colors = self._walker_colors()

        x = int(self.pos)
        y = base_y - len(art)

        self._draw_motion_trail(grid, x, y, art)
        self._draw_text(grid, art, x, y, colors)

        self._draw_point(grid, x + 6, y + 1, self._colorize("▌", "cyan"))

        self._grid = grid

    def cycle(self):
        self.frame += 1
        self.pos += 1

        if self.pos > self.x_size:
            self.pos = -12

        self._build_frame()
        return False


Animator(
    animation=CyberWalker(width=110, height=30),
    speed=Speed.FAST,
    max_loops=0,
)