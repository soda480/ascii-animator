import os
import re
from ascii_animator import Animator, Animation, Speed

class Afuera(Animation):

    def __init__(self):
        self.setup()
    
    @property
    def grid(self):
        return self._grid

    def setup(self):
        filenames = []
        path = 'examples/example3_frames'
        for filename in os.listdir(path):
            if filename.startswith('frame'):
                filenames.append(f'{path}/{filename}')
        self._frames = []
        filenames.sort(key=lambda f: int(re.sub('\D', '', f)))
        for filename in filenames:
            with open(filename) as infile:
                self._frames.append(infile.read().splitlines())
        self._current_frame = 0
        self.load_grid()

    def end(self):
        pass

    def load_grid(self):
        if self._current_frame >= len(self._frames):
            self._current_frame = 0
        self._grid = self._frames[self._current_frame]
        self._current_frame += 1

    def cycle(self):
        self.load_grid()


def main():
    Animator(animation=Afuera(), speed=Speed.FAST)


if __name__ == '__main__':
    main()
