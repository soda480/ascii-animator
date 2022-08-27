from time import sleep
from enum import Enum
from abc import ABC, abstractmethod

from l2term import Lines


class Speed(Enum):
    VERY_SLOW = .4
    SLOW = .11
    NORMAL = .07
    FAST = .03


class Animation(ABC):

    @abstractmethod
    def __init__(self):
        pass  # pragma: no cover

    @abstractmethod
    def cycle(self):
        pass  # pragma: no cover

    @abstractmethod
    def end(self):
        pass  # pragma: no cover

    @property
    def grid(self):
        pass  # pragma: no cover


class Animator(object):

    def __init__(self, animation=None, speed=Speed.NORMAL, start=True):
        """ initialize Animator
        """
        if not isinstance(animation, Animation):
            raise ValueError("animation must be instance of Animation class")
        if not isinstance(speed, Speed):
            raise ValueError("speed must be an instance of Speed Enum")
        self.speed = speed
        self.animation = animation
        if start:
            self.start()

    def _update(self, lines):
        """ update lines on terminal
        """
        for index in range(len(self.animation.grid)):
            lines[index] = self.animation.grid[index]

    def start(self):
        """ animate the animation on the terminal
        """
        with Lines(self.animation.grid, show_index=False) as lines:
            try:
                while True:
                    self.animation.cycle()
                    self._update(lines)
                    sleep(self.speed.value)
            except KeyboardInterrupt:
                self.animation.end()
                self._update(lines)
