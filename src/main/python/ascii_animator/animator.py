import re
import logging
from time import sleep
from enum import Enum
from abc import ABC, abstractmethod

import ascii_magic
from PIL import Image, ImageSequence
from l2term import Lines

logger = logging.getLogger(__name__)


class MaxLoopsProcessed(Exception):
    pass


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


class AsciiAnimation(Animation):

    def __init__(self, path):
        logger.debug('executing AsciiAnimation constructor')
        self._frames = AsciiAnimation.get_ascii_frames_from_image(path)
        self.current = 0
        self.cycle()

    @property
    def grid(self):
        return self._grid

    def cycle(self):
        cycle_complete = False
        if self.current >= len(self._frames):
            self.current = 0
            cycle_complete = True
        self._grid = self._frames[self.current]
        self.current += 1
        return cycle_complete

    @staticmethod
    def get_ascii_frames_from_image(path):
        logger.debug(f'extracting frames from image "{path}" and converting each frame to ascii art')
        frames = []
        image = Image.open(path)
        logger.debug(f'the image "{path}" has a total of {image.n_frames} frames')
        for frame in ImageSequence.Iterator(image):
            ascii_art = ascii_magic.from_image(frame, columns=140, mode=ascii_magic.Modes.ASCII)
            frames.append(ascii_art.split('\n'))
        return frames


class Animator(object):

    def __init__(self, animation=None, speed=Speed.NORMAL, show_axis=False, max_loops=None):
        """ initialize Animator
        """
        logger.debug('executing Animator constructor')
        if not isinstance(animation, Animation):
            raise ValueError("animation must be instance of Animation class")
        if not isinstance(speed, Speed):
            raise ValueError("speed must be an instance of Speed Enum")
        self.speed = speed
        self.animation = animation
        self.show_axis = show_axis
        self.max_loops = max_loops
        self.start()

    def _check_loops(self, cycle_complete):
        """ raise exception if maximum number of loops has been processed
        """
        if not cycle_complete:
            return
        if self.max_loops and self.loop == self.max_loops:
            raise MaxLoopsProcessed('maximum number of loops processed')
        self.loop += 1

    def start(self):
        """ cycle throught the animation and update the terminal using Lines
        """
        logger.debug('starting ascii art animation')
        try:
            logger.debug(f'there are {len(self.animation.grid)} lines in the animation to display')
            with Lines(self.animation.grid, show_index=self.show_axis, show_x_axis=self.show_axis) as lines:
                self.loop = 1
                while True:
                    # update the grid with the next frame
                    cycle_complete = self.animation.cycle()
                    # update terminal via the Lines object
                    for index in range(len(self.animation.grid)):
                        lines[index] = self.animation.grid[index]
                    self._check_loops(cycle_complete)
                    sleep(self.speed.value)

        except KeyboardInterrupt:
            logger.debug('encountered a keyboard interrupt - ending animation')

        except MaxLoopsProcessed:
            logger.debug(f'maximum loops processed {self.loop} - ending animation')
