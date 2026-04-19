import unittest
from mock import patch
from ascii_animator import Animator, Animation


class TestAnimation(Animation):

    def __init__(self):
        self._grid = [[' ' for x in range(3)] for y in range(3)]
        self.current = 0

    @property
    def grid(self):
        return self._grid

    def cycle(self):
        self.current += 1
        if self.current == 2:
            raise KeyboardInterrupt('keyboard interrupt')


class TestAnimator(unittest.TestCase):

    def test__init_Should_RaiseValueError_When_AnimationIsNotInstanceOfAnimation(self, *patches):
        with self.assertRaises(ValueError):
            Animator(animation='something')

    def test__init_Should_RaiseValueError_When_SpeedIsNotInstanceOfSpeedEnum(self, *patches):
        with self.assertRaises(ValueError):
            Animator(animation=TestAnimation(), speed='something')

    @patch('ascii_animator.animator.Lines')
    @patch('ascii_animator.animator.sleep')
    def test__init_Should_UpdateLinesSleepEndAnimation_When_KeyboardInterrupt(self, sleep_patch, lines_patch, *patches):
        test_animation = TestAnimation()
        Animator(animation=test_animation)
        sleep_patch.assert_called()
