import unittest
from mock import patch
from mock import call
from mock import Mock
from ascii_animator import Animator, Animation, Speed


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

    def end(self):
        pass


class TestAnimator(unittest.TestCase):

    def test__init_Should_RaiseValueError_When_AnimationIsNotInstanceOfAnimation(self, *patches):
        with self.assertRaises(ValueError):
            Animator(animation='something')

    def test__init_Should_RaiseValueError_When_SpeedIsNotInstanceOfSpeedEnum(self, *patches):
        with self.assertRaises(ValueError):
            Animator(animation=TestAnimation(), speed='something')

    @patch('ascii_animator.animator.Lines')
    @patch('ascii_animator.animator.sleep')
    @patch('ascii_animator.Animator._update')
    def test__start_Should_EndAnimationAndUpdateLines_When_KeyboardInterrupt(self, update_patch, *patches):
        test_animation = TestAnimation()
        animator = Animator(animation=test_animation, start=False)
        animator.start()
        update_patch.assert_called()

    @patch('ascii_animator.animator.Lines')
    @patch('ascii_animator.animator.sleep')
    @patch('ascii_animator.Animator._update')
    def test__start_Should_CycleAnimationAndUpdateLines_When_Called(self, update_patch, sleep_patch, *patches):
        test_animation = TestAnimation()
        animator = Animator(animation=test_animation, start=False)
        animator.start()
        update_patch.assert_called()
        sleep_patch.assert_called()

    @patch('ascii_animator.animator.Lines')
    def test__update_Should_AssignLines_When_Called(self, *patches):
        test_animation = TestAnimation()
        animator = Animator(animation=test_animation)
        lines = [[], [], []]
        animator._update(lines)
        self.assertEqual(lines[0], test_animation.grid[0])
