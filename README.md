# ascii-animator
[![build](https://github.com/soda480/ascii-animator/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/soda480/ascii-animator/actions/workflows/main.yml)
[![complexity](https://img.shields.io/badge/complexity-Simple:%205-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![PyPI version](https://badge.fury.io/py/ascii-animator.svg)](https://badge.fury.io/py/ascii-animator)
[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)

A simple ASCII text animator.

The `ascii-art-animator` CLI will take as input a GIF image, extract all the frames from it, convert each frame to ASCII art using [ascii-magic](https://pypi.org/project/ascii-magic/), then display each frame to the terminal using [l2term](https://pypi.org/project/l2term/).

### Installation
```bash
pip install ascii_animator
```

### Usage
```
usage: ascii-art-animator [-h] [-s SPEED] [-f FILE] [-d] [-a] [-m MAX_LOOPS] [-c COLUMNS]

Ascii Art Animator from GIF

optional arguments:
  -h, --help            show this help message and exit
  -s SPEED, --speed SPEED
                        speed of the animation: very_slow, slow, normal, fast (default normal)
  -f FILE, --file FILE  the path to a gif file
  -d, --debug           display debug messages to stdout
  -a, --show_axis       display the grid axis
  -m MAX_LOOPS, --max_loops MAX_LOOPS
                        maximum number of loops, set to 0 to loop through image until keyboard interrupt (default 1)
  -c COLUMNS, --columns COLUMNS
                        the number of characters per row (default 150)
```

### Examples

#### ASCII Art Animator

Use `ascii-art-animator` to convert the following [GIF image](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich.gif) to an ascii animation and demonstrate the use of the optional arguments.
* show x and y axis
* loop through the image 3 times 
* set columns to 100 characters

```bash
ascii-art-animator -f docs/images/marcovich.gif -a -m 3 -c 100
```

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich-exec.gif)

#### [Equalizer Bars Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example2.py)

Create an animation by subclassing the `Animation` class to resemble symmetrical equalizer bars and display it to the terminal using the `Animator` class.

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example2.gif)

#### [Matrix Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example3.py)

Create an animation by subclassing the `Animation` class to resemble the Matrix and display it to the terminal using the `Animator` class.

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example3.gif)

#### [Game-Of-Life](https://github.com/soda480/game-of-life)

A Conway Game-Of-Life implementation that uses `ascii_animator` to display the game to the terminal.

### Development

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```bash
docker image build \
-t \
ascii-animator:latest .
```

Run the Docker container:
```bash
docker container run \
--rm \
-it \
-v $PWD:/code \
ascii-animator:latest \
bash
```

Execute the build:
```sh
pyb -X
```
