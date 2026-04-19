from math import atan2, cos, sin, sqrt
from ascii_animator import Animator, Animation, Speed


class ChromaticVortexReactor(Animation):
    RESET = "\033[0m"

    COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }

    def __init__(self, width=120, height=34):
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

    def _clamp(self, value, low, high):
        if value < low:
            return low
        if value > high:
            return high
        return value

    def _empty(self):
        return [[" " for _ in range(self.x_size)] for _ in range(self.y_size)]

    def _draw(self, grid, x, y, value):
        if 0 <= x < self.x_size and 0 <= y < self.y_size:
            grid[y][x] = value

    def _glyph(self, energy):
        if energy < 0.10:
            return " "
        if energy < 0.20:
            return "."
        if energy < 0.30:
            return "·"
        if energy < 0.42:
            return ":"
        if energy < 0.54:
            return "*"
        if energy < 0.66:
            return "◆"
        if energy < 0.78:
            return "●"
        if energy < 0.90:
            return "◉"
        return "✦"

    def _spectral_color(self, phase):
        phase = phase % 6.0
        if phase < 1.0:
            return "red"
        if phase < 2.0:
            return "yellow"
        if phase < 3.0:
            return "green"
        if phase < 4.0:
            return "cyan"
        if phase < 5.0:
            return "blue"
        return "magenta"

    def _energy_color(self, energy, angle, dist):
        phase = (
            energy * 2.3
            + angle * 0.9
            + dist * 0.08
            + self.frame * 0.06
        )
        return self._spectral_color(phase)

    def _draw_background_flux(self, grid, cx, cy):
        for y in range(self.y_size):
            for x in range(self.x_size):
                dx = x - cx
                dy = y - cy
                dist = sqrt(dx * dx + dy * dy)

                if dist < 8:
                    continue

                field = (
                    sin((x * 0.10) + (self.frame / 9.0))
                    + sin((y * 0.16) - (self.frame / 11.0))
                    + sin((dist * 0.22) - (self.frame / 7.0))
                ) / 3.0

                if field > 0.72:
                    color = self._spectral_color((x * 0.03) + (y * 0.02) + (self.frame * 0.04))
                    self._draw(grid, x, y, self._colorize("·", color))
                elif field < -0.78 and (x + y + self.frame) % 3 == 0:
                    self._draw(grid, x, y, self._colorize(".", "blue"))

    def _draw_core(self, grid, cx, cy):
        pulse = 4.0 + abs(sin(self.frame / 4.0)) * 2.2

        for y in range(self.y_size):
            for x in range(self.x_size):
                dx = x - cx
                dy = y - cy
                dist = sqrt(dx * dx + dy * dy)
                angle = atan2(dy, dx)

                if dist > pulse * 1.2:
                    continue

                phase = sin((self.frame / 2.5) + dist * 2.7 + angle * 5.0)

                if dist < pulse * 0.33:
                    if phase > 0.4:
                        ch, color = "✦", "white"
                    elif phase > 0.1:
                        ch, color = "◉", "yellow"
                    elif phase > -0.2:
                        ch, color = "●", "cyan"
                    else:
                        ch, color = "◆", "magenta"
                elif dist < pulse * 0.65:
                    if phase > 0.55:
                        ch, color = "◉", "yellow"
                    elif phase > 0.15:
                        ch, color = "●", "red"
                    elif phase > -0.15:
                        ch, color = "◆", "green"
                    else:
                        ch, color = "*", "blue"
                else:
                    if phase > 0.45:
                        ch, color = "◆", "cyan"
                    elif phase > 0.05:
                        ch, color = "●", "magenta"
                    else:
                        ch, color = "*", "red"

                if (x + y + self.frame) % 7 == 0:
                    ch, color = "✦", "white"

                self._draw(grid, x, y, self._colorize(ch, color))

    def _draw_vortex_rings(self, grid, cx, cy):
        base_radii = [8.5, 12.5, 17.5, 23.0]

        for ring_index, base_radius in enumerate(base_radii):
            radius = base_radius + sin((self.frame / (5.0 + ring_index)) + ring_index) * (0.8 + ring_index * 0.25)
            thickness = 0.9 + (ring_index * 0.1)
            spin = self.frame / (6.0 - min(ring_index, 3))

            for y in range(self.y_size):
                for x in range(self.x_size):
                    dx = x - cx
                    dy = (y - cy) / (0.58 + ring_index * 0.035)
                    dist = sqrt(dx * dx + dy * dy)

                    if not (radius - thickness < dist < radius + thickness):
                        continue

                    angle = atan2(dy, dx)
                    wave = sin((angle * (7 + ring_index * 2)) - spin + dist * 0.9)
                    ripple = sin((dist * 1.6) + (self.frame / 3.5) - angle * 2.0)
                    energy = (wave * 0.6 + ripple * 0.4 + 1.0) / 2.0

                    if energy < 0.22:
                        continue

                    ch = self._glyph(energy)
                    color = self._energy_color(energy + (ring_index * 0.1), angle, dist)

                    if ring_index % 2 == 1 and energy > 0.82:
                        ch = "✦"
                        color = "white"

                    self._draw(grid, x, y, self._colorize(ch, color))

    def _draw_spiral_arms(self, grid, cx, cy):
        arms = 5
        max_radius = min(self.x_size, self.y_size) * 0.48

        for arm in range(arms):
            arm_phase = arm * 1.256637

            for step in range(6, int(max_radius)):
                radius = step
                angle = arm_phase + (radius * 0.27) + (self.frame / 8.0)

                x = int(cx + cos(angle) * radius * 1.15)
                y = int(cy + sin(angle) * radius * 0.62)

                energy = 1.0 - (radius / max_radius)
                if energy < 0.08:
                    continue

                if energy > 0.72:
                    ch = "✦"
                elif energy > 0.48:
                    ch = "◉"
                elif energy > 0.28:
                    ch = "◆"
                else:
                    ch = "·"

                color = self._spectral_color((arm * 0.8) + (radius * 0.04) + (self.frame * 0.07))
                self._draw(grid, x, y, self._colorize(ch, color))

    def _draw_energy_spokes(self, grid, cx, cy):
        spoke_count = 12

        for i in range(spoke_count):
            angle = (i / spoke_count) * 6.28318 + (self.frame / 18.0)
            wobble = sin((self.frame / 6.0) + i) * 0.12

            for step in range(5, min(self.x_size, self.y_size) // 2):
                radius = step
                x = int(cx + cos(angle + wobble) * radius * 1.12)
                y = int(cy + sin(angle + wobble) * radius * 0.60)

                intensity = 1.0 - (radius / (min(self.x_size, self.y_size) / 2.0))
                if intensity < 0.10:
                    continue

                if (step + i + self.frame) % 4 != 0:
                    continue

                if intensity > 0.72:
                    ch, color = "|", "white"
                elif intensity > 0.50:
                    ch, color = "!", "cyan"
                elif intensity > 0.30:
                    ch, color = ":", "magenta"
                else:
                    ch, color = ".", "blue"

                self._draw(grid, x, y, self._colorize(ch, color))

    def _draw_orbiting_shards(self, grid, cx, cy):
        shard_count = 28

        for i in range(shard_count):
            angle = (i * 0.2244) + (self.frame / 9.0)
            radius = 26 + sin((self.frame / 4.0) + i * 0.8) * 4 + (i % 5)
            x = int(cx + cos(angle) * radius * 1.22)
            y = int(cy + sin(angle) * radius * 0.70)

            if i % 6 == 0:
                ch, color = "✦", "white"
            elif i % 5 == 0:
                ch, color = "◉", "yellow"
            elif i % 3 == 0:
                ch, color = "◆", "magenta"
            elif i % 2 == 0:
                ch, color = "●", "cyan"
            else:
                ch, color = "*", "green"

            self._draw(grid, x, y, self._colorize(ch, color))

            trail_angle = angle - 0.18
            tx = int(cx + cos(trail_angle) * (radius - 1.3) * 1.22)
            ty = int(cy + sin(trail_angle) * (radius - 1.3) * 0.70)
            self._draw(grid, tx, ty, self._colorize("·", "blue"))

    def _draw_feed_beams(self, grid, cx, cy):
        lanes = [-18, -12, -7, 0, 7, 12, 18]

        for idx, lane in enumerate(lanes):
            phase = self.frame / 5.0 + idx * 0.9

            for step in range(self.y_size // 2):
                intensity = 1.0 - step / (self.y_size / 2.0)
                if intensity < 0.08:
                    continue

                wobble = sin(step / 3.7 + phase) * (1.0 + abs(lane) * 0.03)
                pull = lane * max(0.12, 1.0 - (step / (self.y_size / 2.2)))

                x = int(cx + pull + wobble)

                top = int(cy - 7 - step)
                bot = int(cy + 7 + step)

                color_phase = idx + step * 0.04 + self.frame * 0.06
                color = self._spectral_color(color_phase)

                if intensity > 0.76:
                    ch = "|"
                elif intensity > 0.52:
                    ch = "!"
                elif intensity > 0.30:
                    ch = ":"
                else:
                    ch = "."

                if 0 <= x < self.x_size:
                    if 0 <= top < self.y_size:
                        self._draw(grid, x, top, self._colorize(ch, color))
                    if 0 <= bot < self.y_size:
                        self._draw(grid, x, bot, self._colorize(ch, color))

    def _draw_shockwaves(self, grid, cx, cy):
        for offset in (0, 11, 23):
            radius = ((self.frame * 1.4) + offset) % 44
            if radius < 6:
                continue

            thickness = 0.45
            for y in range(self.y_size):
                for x in range(self.x_size):
                    dx = x - cx
                    dy = (y - cy) / 0.64
                    dist = sqrt(dx * dx + dy * dy)

                    if radius - thickness < dist < radius + thickness:
                        if (x + y + offset + self.frame) % 3 == 0:
                            color = self._spectral_color((radius * 0.08) + (self.frame * 0.04))
                            self._draw(grid, x, y, self._colorize(".", color))

    def _build_frame(self):
        grid = self._empty()

        cx = self.x_size / 2.0
        cy = self.y_size / 2.0

        self._draw_background_flux(grid, cx, cy)
        self._draw_shockwaves(grid, cx, cy)
        self._draw_vortex_rings(grid, cx, cy)
        self._draw_spiral_arms(grid, cx, cy)
        self._draw_energy_spokes(grid, cx, cy)
        self._draw_feed_beams(grid, cx, cy)
        self._draw_orbiting_shards(grid, cx, cy)
        self._draw_core(grid, cx, cy)

        self._grid = grid

    def cycle(self):
        self.frame += 1
        self._build_frame()
        return False


Animator(
    animation=ChromaticVortexReactor(width=120, height=34),
    speed=Speed.FAST,
    max_loops=0,
)