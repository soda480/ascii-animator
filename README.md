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
ascii-art-animator --help
usage: ascii-art-animator [-h] [-s SPEED] [-f FILE] [-d]

Ascii Art Animator from GIF

optional arguments:
  -h, --help            show this help message and exit
  -s SPEED, --speed SPEED
                        speed of the animation: very_slow, slow, normal, fast (default normal)
  -f FILE, --file FILE  the path to a gif file
  -d, --debug           display debug messages to stdout
```

### Examples

#### ASCII conversion and animation of GIF images

Convert the following [GIF image](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich.gif)

```bash
ascii-art-animator -f docs/images/marcovich.gif
```

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich-execution.gif)

Convert the following [GIF image](https://github.com/soda480/ascii-animator/blob/main/docs/images/afuera.gif?raw=true)

```bash
ascii-art-animator -f docs/images/afuera.gif -s fast
```

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/afuera-execution.gif)

#### Game-Of-Life

A Conway [Game-Of-Life](https://github.com/soda480/game-of-life) implementation that uses `ascii_animator` to display the game to the terminal.

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
