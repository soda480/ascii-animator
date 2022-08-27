from ascii_animator import Animator, Animation, Speed


class Dancer(Animation):

    def __init__(self, y_size, x_size):
        self.y_size = y_size
        self.x_size = x_size
        self.setup()
        self._frame = 1
    
    @property
    def grid(self):
        return self._grid

    def setup(self):
        self._grid = [[' ' for x in range(self.x_size)] for y in range(self.y_size)]
        self._grid[0][4] = chr(65077)  # ︵
        self._grid[1][2] = '('
        self._grid[1][3] = chr(9679)  # ● 
        self._grid[1][4] = chr(8255)  # ‿
        self._grid[1][5] = chr(9679)  # ●
        self._grid[1][6] = ')'
        self._grid[2][2] = '<'
        self._grid[2][3] = '|'
        self._grid[2][5] = '|'
        self._grid[2][6] = '>'
        self._grid[3][3] = chr(9585)  # ╱
        self._grid[3][5] = chr(9586)  # ╲

    def end(self):
        self.setup()

    def frame1(self):
        self._grid[0][4] = chr(65077)  # ︵
        self._grid[1][1] = chr(9586)  # ╲
        self._grid[1][7] = ' '
        self._grid[2][2] = ' '
        self._grid[2][3] = '('
        self._grid[2][5] = '('
        self._grid[2][6] = '>'
        self._grid[3][3] = chr(9585)  # ╱
        self._grid[3][4] = ' '
        self._grid[3][5] = chr(9586)  # ╲

    def frame2(self):
        self._grid[0][4] = chr(65083)  # ︻
        self._grid[1][1] = ' '
        self._grid[1][7] = chr(9585)  # ╱
        self._grid[2][2] = '<'
        self._grid[2][3] = ')'
        self._grid[2][5] = ')'
        self._grid[2][6] = ' '
        self._grid[3][3] = chr(65295)  # ／
        self._grid[3][4] = chr(65340)  # ＼
        self._grid[3][5] = ' '

    def cycle(self):
        function = getattr(self, f'frame{self._frame}', self.frame1)
        function()
        if function.__name__ == 'frame1':
            self._frame = 1 
        self._frame += 1


def main():
    Animator(animation=Dancer(6, 9), speed=Speed.VERY_SLOW)


if __name__ == '__main__':  # pragma: no cover
    main()
