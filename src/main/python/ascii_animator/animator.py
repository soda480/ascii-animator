import os
import re
import inspect
import logging
from time import sleep
from enum import Enum
from abc import ABC, abstractmethod

import ascii_magic
from PIL import Image, ImageSequence
from list2term import Lines

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
    def cycle(self):
        pass  # pragma: no cover

    @property
    def grid(self):
        pass  # pragma: no cover


class AsciiAnimation(Animation):

    def __init__(self, path, columns=150):
        """ constructor
        """
        logger.debug('executing AsciiAnimation constructor')
        if not os.path.isfile(path):
            raise ValueError(f'the path "{path}" is not valid')
        self._image = Image.open(path)
        self.columns = columns
        self._current = 0
        self._image_processed = False
        self._number_of_frames = self._image.n_frames
        self._frames = []
        self.cycle()

    def __del__(self):
        """ destructor
        """
        logger.debug('executing AsciiAnimation destructor')
        if hasattr(self, '_image') and self._image:
            self._image.close()

    @property
    def grid(self):
        return self._grid

    def cycle(self):
        """ assign grid the next frame and return if a full cycle of the image has completed
        """
        if not self._image_processed:
            frame = ImageSequence.Iterator(self._image)[self._current]
            ascii_art = ascii_magic.from_image(frame, columns=self.columns, mode=ascii_magic.Modes.ASCII)
            self._frames.append(ascii_art.split('\n'))
            if len(self._frames) == self._number_of_frames:
                self._image_processed = True
                self._image.close()
            self._grid = self._frames[self._current]
            self._current += 1
            return self._image_processed
        cycle_complete = False
        if self._current == self._number_of_frames:
            self._current = 0
            cycle_complete = True
        self._grid = self._frames[self._current]
        self._current += 1
        return cycle_complete


class Animator:

    def __init__(self, animation=None, speed=Speed.NORMAL, show_axis=False, max_loops=None, first_cycle_sleep=True):
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
        # control if animator should sleep after first loop
        # some animations first cycle is slow thus a sleep is not necessary
        # AsciiAnimation first cycle loads the image into memory
        # this process is inherently slow thus sleeping is not necessary
        self.first_cycle_sleep = first_cycle_sleep
        self.start()

    def _check_loops(self, cycle_complete):
        """ raise exception if maximum number of loops has been processed
        """
        if not cycle_complete:
            return
        if self.max_loops and self.loop >= self.max_loops:
            raise MaxLoopsProcessed('maximum number of loops processed')
        self.loop += 1

    def _sleep(self):
        """ determine if execution should sleep
        """
        if self.loop == 1 and not self.first_cycle_sleep:
            return
        sleep(self.speed.value)

    def _get_max_chars(self):
        """ return max chars for animation
        """
        if hasattr(self.animation, 'columns'):
            max_chars = self.animation.columns
        elif hasattr(self.animation, 'x_size'):
            max_chars = self.animation.x_size
        else:
            max_chars = None
        return max_chars

    def _update_terminal(self, lines, cycle_complete):
        """ update lines
        """
        # update terminal via the Lines object
        for index, _ in enumerate(self.animation.grid):
            lines[index] = self.animation.grid[index]
        self._check_loops(cycle_complete)
        self._sleep()

    def start(self):
        """ cycle throught the animation and update the terminal using Lines
        """
        logger.debug('starting ascii art animation')
        try:
            logger.debug(f'there are {len(self.animation.grid)} lines in the animation to display')
            with Lines(self.animation.grid, show_index=self.show_axis, show_x_axis=self.show_axis, max_chars=self._get_max_chars()) as lines:
                self.loop = 1
                while True:
                    # update the grid with the next frame
                    if inspect.isgeneratorfunction(self.animation.cycle):
                        # support case where cycle is a generator
                        for cycle_complete in self.animation.cycle():
                            self._update_terminal(lines, cycle_complete)
                        self.animation.reset()
                    else:
                        cycle_complete = self.animation.cycle()
                        self._update_terminal(lines, cycle_complete)

        except KeyboardInterrupt:
            logger.debug('encountered a keyboard interrupt - ending animation')

        except MaxLoopsProcessed:
            logger.debug(f'maximum loops processed {self.loop - 1} - ending animation')
