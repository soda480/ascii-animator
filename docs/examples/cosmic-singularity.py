from math import atan2, cos, sin, sqrt
from ascii_animator import Animator, Animation, Speed


class CosmicSingularity(Animation):
    RESET = "\033[0m"

    COLORS = {
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "yellow": "\033[93m",
        "white": "\033[97m",
        "red": "\033[91m",
        "green": "\033[92m",
    }

    def __init__(self, width=110, height=32):
        self.x_size = width
        self.y_size = height
        self.frame = 0
        self._grid = []
        self._build_frame()

    @property
    def grid(self):
        return self._grid

    def _colorize(self, ch, color):
        return f"{self.COLORS[color]}{ch}{self.RESET}"

    def _clamp(self, v, lo, hi):
        return lo if v < lo else hi if v > hi else v

    def _empty(self):
        return [[" " for _ in range(self.x_size)] for _ in range(self.y_size)]

    def _draw(self, grid, x, y, value):
        if 0 <= x < self.x_size and 0 <= y < self.y_size:
            grid[y][x] = value

    def _glyph(self, energy):
        if energy < 0.15:
            return " "
        if energy < 0.30:
            return "."
        if energy < 0.45:
            return "·"
        if energy < 0.60:
            return "◆"
        if energy < 0.75:
            return "●"
        if energy < 0.88:
            return "◉"
        return "✦"

    def _color(self, energy):
        if energy < 0.25:
            return "blue"
        if energy < 0.50:
            return "cyan"
        if energy < 0.70:
            return "magenta"
        if energy < 0.90:
            return "yellow"
        return "white"

    def _draw_feeder_jets(self, grid, cx, cy, photon):
        stream_offsets = [0, -2, 2, -4, 4, -7, 7]
        max_steps = self.y_size // 2

        for i, offset in enumerate(stream_offsets):
            phase = self.frame / 6.0 + (i * 0.9)

            for step in range(max_steps):
                intensity = 1 - step / max_steps
                if intensity < 0.05:
                    continue

                wobble = sin(step / 4.0 + phase) * (1.0 + abs(offset) * 0.05)
                inward = offset * max(0.2, 1 - step / max_steps)

                x = int(cx + inward + wobble)

                top = int(cy - photon - 1 - step)
                bot = int(cy + photon + 1 + step)

                if intensity > 0.7:
                    ch, color = "|", "white"
                elif intensity > 0.5:
                    ch, color = "!", "cyan"
                elif intensity > 0.3:
                    ch, color = ":", "blue"
                else:
                    ch, color = ".", "magenta"

                if 0 <= x < self.x_size:
                    if 0 <= top < self.y_size:
                        grid[top][x] = self._colorize(ch, color)
                    if 0 <= bot < self.y_size:
                        grid[bot][x] = self._colorize(ch, color)

    def _build_frame(self):
        grid = self._empty()

        cx = self.x_size / 2
        cy = self.y_size / 2

        spin = self.frame / 5.0
        pulse = 1 + abs(sin(self.frame / 6.0)) * 0.25

        inner = 4.2 * pulse
        photon = 5.6 * pulse
        outer = min(self.x_size, self.y_size) * 0.36
        tilt = 0.42

        for y in range(self.y_size):
            for x in range(self.x_size):
                dx = x - cx
                dy = (y - cy) / tilt
                dist = sqrt(dx * dx + dy * dy)
                angle = atan2(dy, dx)

                # --- ENHANCED CORE COLOR LOGIC ---
                if dist < inner * 0.72:
                    energy = sin(self.frame / 3.0 + dist * 2.5 + angle * 4.0)

                    # rotating color band
                    color_phase = (angle + self.frame / 8.0) % (6.28)

                    if energy > 0.7:
                        ch, color = "✦", "white"
                    elif energy > 0.4:
                        ch, color = "◉", "yellow"
                    elif energy > 0.1:
                        ch, color = "●", "red"
                    elif energy > -0.2:
                        ch, color = "◆", "green"
                    elif energy > -0.5:
                        ch, color = "●", "cyan"
                    else:
                        ch, color = "◆", "blue"

                    # add flicker
                    if (x + y + self.frame) % 7 == 0:
                        ch, color = "✦", "white"

                    grid[y][x] = self._colorize(ch, color)
                    continue

                # --- PHOTON RING ---
                if inner * 0.72 <= dist < photon:
                    flicker = sin(angle * 12 - spin * 2 + dist * 2)

                    if flicker > 0.6:
                        ch, color = "✦", "white"
                    elif flicker > 0.3:
                        ch, color = "◉", "yellow"
                    elif flicker > 0:
                        ch, color = "●", "red"
                    else:
                        ch, color = "◆", "cyan"

                    grid[y][x] = self._colorize(ch, color)
                    continue

                # --- DISK ---
                if photon < dist < outer:
                    swirl = sin(dist * 1.2 - angle * 4.5 - spin)
                    ripple = sin(dist * 2.4 + spin * 1.5)
                    turbulence = sin(dx * 0.15 + dy * 0.1 + self.frame / 6.0)

                    falloff = 1 - ((dist - photon) / (outer - photon))

                    energy = (
                        swirl * 0.3 +
                        ripple * 0.2 +
                        turbulence * 0.2 +
                        falloff * 1.0
                    )

                    normalized = self._clamp((energy + 1) / 2, 0, 1)

                    ch = self._glyph(normalized)
                    color = self._color(normalized)

                    if ch != " ":
                        grid[y][x] = self._colorize(ch, color)

        # halo
        halo = outer + 3 + abs(sin(self.frame / 8.0)) * 2
        for y in range(self.y_size):
            for x in range(self.x_size):
                dx = x - cx
                dy = (y - cy) / 0.6
                dist = sqrt(dx * dx + dy * dy)

                if halo - 0.5 < dist < halo + 0.5 and grid[y][x] == " ":
                    grid[y][x] = self._colorize(".", "magenta")

        # jets
        self._draw_feeder_jets(grid, cx, cy, photon)

        # debris
        for i in range(24):
            angle = i * 0.26 + self.frame / 10.0
            radius = outer + 2 + sin(self.frame / 4.0 + i) * 2

            x = int(cx + cos(angle) * radius * 1.4)
            y = int(cy + sin(angle) * radius * 0.6)

            if i % 5 == 0:
                val = self._colorize("◉", "white")
            elif i % 3 == 0:
                val = self._colorize("◆", "yellow")
            else:
                val = self._colorize(".", "cyan")

            self._draw(grid, x, y, val)

        self._grid = grid

    def cycle(self):
        self.frame += 1
        self._build_frame()
        return False


Animator(
    animation=CosmicSingularity(),
    speed=Speed.FAST,
    max_loops=0,
)