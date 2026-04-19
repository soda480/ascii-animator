import sys
import argparse
import traceback
import logging

from ascii_animator import Animator, Speed, AsciiAnimation

logger = logging.getLogger(__name__)


def get_speed(value):
    speeds = {
        'very_slow': Speed.VERY_SLOW,
        'slow': Speed.SLOW,
        'normal': Speed.NORMAL,
        'fast': Speed.FAST
    }
    speed = speeds.get(value)
    if not speed:
        raise argparse.ArgumentTypeError('speed must be: very_slow, slow, normal, fast')
    return speed


def main():
    parser = argparse.ArgumentParser(description='Ascii Art Animator from GIF')
    parser.add_argument('-s', '--speed', type=str, default='normal', help='speed of the animation: very_slow, slow, normal, fast (default normal)')
    parser.add_argument('-f', '--file', type=str, help='the path to a gif file')
    parser.add_argument('-d', '--debug', action='store_true', help='display debug messages to stdout')
    parser.add_argument('-a', '--show_axis', action='store_true', help='display the grid axis')
    parser.add_argument('-m', '--max_loops', type=int, default=1, help='maximum number of loops, set to 0 to loop through image until keyboard interrupt (default 1)')
    parser.add_argument('-c', '--columns', type=int, default=150, help='the number of characters per row (default 150)')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    try:
        speed = get_speed(args.speed)
        Animator(
            animation=AsciiAnimation(args.file, columns=args.columns),
            speed=speed,
            show_axis=args.show_axis,
            max_loops=args.max_loops,
            first_cycle_sleep=False)

    except argparse.ArgumentError:
        parser.print_help()

    except Exception as exception:
        print(exception)
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
