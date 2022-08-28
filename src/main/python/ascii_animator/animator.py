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

    @property
    def grid(self):
        pass  # pragma: no cover


class Animator(object):

    def __init__(self, animation=None, speed=Speed.NORMAL, show_index=False):
        """ initialize Animator
        """
        if not isinstance(animation, Animation):
            raise ValueError("animation must be instance of Animation class")
        if not isinstance(speed, Speed):
            raise ValueError("speed must be an instance of Speed Enum")
        self.speed = speed
        self.animation = animation
        self.show_index = show_index
        self.start()

    def start(self):
        """ cycle throught the animation and update the terminal using Lines
        """
        with Lines(self.animation.grid, show_index=self.show_index) as lines:
            try:
                while True:
                    # cycle through the animation by updating a grid frame
                    self.animation.cycle()
                    # update terminal using the Lines object
                    for index in range(len(self.animation.grid)):
                        lines[index] = self.animation.grid[index]
                    sleep(self.speed.value)
            except KeyboardInterrupt:
                pass
