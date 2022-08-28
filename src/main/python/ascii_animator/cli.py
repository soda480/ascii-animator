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
    parser = argparse.ArgumentParser(description="Ascii Art Animator from GIF")
    parser.add_argument("-s", "--speed", type=str, default='normal', help="speed of the animation: very_slow, slow, normal, fast (default normal)")
    parser.add_argument("-f", "--file", type=str, help="the path to a gif file")
    parser.add_argument("-d", "--debug", action="store_true", help="display debug messages to stdout")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    try:
        speed = get_speed(args.speed)
        Animator(
            animation=AsciiAnimation(args.file),
            speed=speed)

    except argparse.ArgumentError:
        parser.print_help()

    except Exception as exception:
        print(exception)
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
