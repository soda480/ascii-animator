from math import sin, sqrt
from ascii_animator import Animator, Animation, Speed


class PlasmaWave(Animation):
    RESET = "\033[0m"

    COLORS = {
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "yellow": "\033[93m",
        "white": "\033[97m",
    }

    def __init__(self, width=100, height=30):
        self.x_size = width
        self.y_size = height
        self.frame = 0
        self.palette = " .,:;-~=+*#%@"
        self._grid = []
        self._build_frame()

    @property
    def grid(self):
        return self._grid

    def _clamp(self, value, low, high):
        if value < low:
            return low
        if value > high:
            return high
        return value

    def _colorize(self, ch, color_name):
        return f"{self.COLORS[color_name]}{ch}{self.RESET}"

    def _sample(self, x, y, cx, cy):
        dx = x - cx
        dy = y - cy
        dist = sqrt(dx * dx + dy * dy)

        v1 = sin((x / 7.0) + (self.frame / 4.0))
        v2 = sin((y / 5.0) - (self.frame / 5.5))
        v3 = sin(((x + y) / 9.0) + (self.frame / 6.0))
        v4 = sin(dist / 3.2 - (self.frame / 2.8))
        v5 = sin((x * 0.12) - (y * 0.09) + (self.frame / 7.0))
        v6 = sin((dist / 6.5) + (self.frame / 3.3))

        value = (v1 + v2 + v3 + v4 + v5 + v6) / 6.0
        return value, dist

    # 🔥 UPDATED: soft color fade instead of hard cutoff
    def _char_and_color(self, value, dist, cx, cy):
        normalized = (value + 1.0) / 2.0
        normalized = self._clamp(normalized, 0.0, 1.0)

        index = int(normalized * (len(self.palette) - 1))
        ch = self.palette[index]

        base_radius = min(self.x_size, self.y_size) * 0.28
        fade_radius = base_radius * 1.25

        # --- FULL COLOR CORE ---
        if dist <= base_radius:
            if normalized < 0.18:
                return self._colorize(ch, "blue")
            if normalized < 0.38:
                return self._colorize(ch, "cyan")
            if normalized < 0.62:
                return self._colorize(ch, "magenta")
            if normalized < 0.82:
                return self._colorize(ch, "yellow")
            return self._colorize(ch, "white")

        # --- SUBTLE COLOR BLEED ---
        if dist <= fade_radius:
            if normalized > 0.65:
                if normalized > 0.85:
                    return self._colorize(ch, "white")
                elif normalized > 0.75:
                    return self._colorize(ch, "yellow")
                else:
                    return self._colorize(ch, "magenta")
            return ch

        # --- OUTER GRAYSCALE ---
        return ch

    def _draw_core(self, grid, cx, cy):
        pulse = 2.5 + abs(sin(self.frame / 3.0)) * 5.0

        for y in range(self.y_size):
            for x in range(self.x_size):
                dx = x - cx
                dy = y - cy
                dist = sqrt(dx * dx + dy * dy)

                if dist < pulse * 0.55:
                    grid[y][x] = self._colorize("@", "white")
                elif dist < pulse * 0.95:
                    grid[y][x] = self._colorize("#", "yellow")
                elif dist < pulse * 1.45:
                    grid[y][x] = self._colorize("*", "magenta")

    def _draw_ring(self, grid, cx, cy):
        ring_radius = 8 + abs(sin(self.frame / 4.0)) * 10
        thickness = 1.2

        for y in range(self.y_size):
            for x in range(self.x_size):
                dx = x - cx
                dy = y - cy
                dist = sqrt(dx * dx + dy * dy)

                if ring_radius - thickness < dist < ring_radius + thickness:
                    grid[y][x] = self._colorize("+", "cyan")

    def _draw_streaks(self, grid, cx, cy):
        angle = self.frame / 5.0

        for i in range(3):
            phase = angle + (i * 2.09439)

            for step in range(4, min(self.x_size, self.y_size)):
                x = int(cx + sin(phase) * step * 1.8)
                y = int(cy + sin(phase + 1.5708) * step * 0.8)

                if 0 <= x < self.x_size and 0 <= y < self.y_size:
                    if step % 5 == 0:
                        grid[y][x] = self._colorize("@", "white")
                    elif step % 3 == 0:
                        grid[y][x] = self._colorize("#", "yellow")
                    else:
                        grid[y][x] = self._colorize("*", "magenta")

    def _build_frame(self):
        grid = []

        cx = (self.x_size / 2.0) + sin(self.frame / 11.0) * 3.0
        cy = (self.y_size / 2.0) + sin(self.frame / 13.0) * 1.5

        for y in range(self.y_size):
            row = []

            for x in range(self.x_size):
                value, dist = self._sample(x, y, cx, cy)

                fade = 1.0 - min(dist / max(self.x_size, self.y_size), 0.35)
                value = self._clamp(value * (1.0 + (fade * 0.35)), -1.0, 1.0)

                row.append(self._char_and_color(value, dist, cx, cy))

            grid.append(row)

        self._draw_ring(grid, cx, cy)
        self._draw_streaks(grid, cx, cy)
        self._draw_core(grid, cx, cy)

        self._grid = grid

    def cycle(self):
        self.frame += 1
        self._build_frame()
        return False


Animator(
    animation=PlasmaWave(width=120, height=34),
    speed=Speed.SLOW,
    max_loops=0,
)