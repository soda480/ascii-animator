import re
import logging
from time import sleep
from enum import Enum
from abc import ABC, abstractmethod

import ascii_magic
from PIL import Image, ImageSequence
from l2term import Lines

logger = logging.getLogger(__name__)


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
        self.current = None
        self.cycle()

    @property
    def grid(self):
        return self._grid

    def cycle(self):
        if self.current is None or self.current >= len(self._frames):
            self.current = 0
        self._grid = self._frames[self.current]
        self.current += 1

    @staticmethod
    def get_ascii_frames_from_image(path):
        logger.debug(f'extracting frames from image "{path}" and converting each frame to ascii art')
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        frames = []
        image = Image.open(path)
        logger.debug(f'the image "{path}" has {image.n_frames} frames')
        for frame in ImageSequence.Iterator(image):
            ascii_art = ascii_magic.from_image(frame, columns=140)
            ascii_art_sanitized = ansi_escape.sub('', ascii_art)
            frames.append(ascii_art_sanitized.split("\n"))
        return frames


class Animator(object):

    def __init__(self, animation=None, speed=Speed.NORMAL, show_index=False):
        """ initialize Animator
        """
        logger.debug('executing Animator constructor')
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
                logger.debug('starting ascii art animation')
                while True:
                    # cycle through the animation by updating a grid frame
                    self.animation.cycle()
                    # update terminal using the Lines object
                    for index in range(len(self.animation.grid)):
                        lines[index] = self.animation.grid[index]
                    sleep(self.speed.value)
            except KeyboardInterrupt:
                pass
