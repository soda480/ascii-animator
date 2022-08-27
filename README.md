# ascii-animator
[![complexity](https://img.shields.io/badge/complexity-Simple:%204-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)

A simple ASCII text animator.

### Installation
```bash
pip install ascii_animator
```
#### Example1

A Conway [Game-Of-Life](https://github.com/soda480/game-of-life) implementation that uses `ascii_animator` to display the game to the terminal.

#### [example2](https://github.com/soda480/ascii-animator/blob/main/examples/example2.py)

A walking man animation.

![example1](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example2.gif)

#### [example3](https://github.com/soda480/ascii-animator/blob/main/examples/example3.py)

A animation extracted from a GIF image.

![example3](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example3.gif)

### Development

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t \
ascii-animator:latest .
```

Run the Docker container:
```sh
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
