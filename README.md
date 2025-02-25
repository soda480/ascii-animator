<div align="center" style="padding: 20px 0;">
  <h1 style="font-size: 2.5em; margin-bottom: 0.2em; font-family: Arial, sans-serif;">ascii-animator - A simple ASCII text animator</h1>
  
  <div style="margin: 20px 0;">
    <a href="https://github.com/soda480/ascii-animator/actions/workflows/main.yml">
      <img src="https://github.com/soda480/ascii-animator/actions/workflows/main.yml/badge.svg?branch=main" alt="build+test" style="margin: 5px;">
    </a>
    <a href="https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity">
      <img src="https://img.shields.io/badge/complexity-A-brightgreen" alt="complexity" style="margin: 5px;">
    </a>
    <a href="https://pypi.org/project/bandit/">
      <img src="https://img.shields.io/badge/vulnerabilities-None-brightgreen" alt="vulnerabilities" style="margin: 5px;">
    </a>
    <a href="https://badge.fury.io/py/ascii-animator">
      <img src="https://badge.fury.io/py/ascii-animator.svg" alt="PyPI version" style="margin: 5px;">
    </a>
    <a href="https://www.python.org/downloads/">
      <img src="https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-teal" alt="python" style="margin: 5px;">
    </a>
  </div>
  
  <img src="https://github.com/user-attachments/assets/61de12c5-c7e7-4464-ae80-bc516a791bea" alt="ascii-animator image" style="width: 400px; border: 1px solid #ddd; border-radius: 5px; margin-top: 20px;">
</div>

<br>
The `ascii-art-animator` CLI will take as input a GIF image, extract all the frames from it, convert each frame to ASCII art using [ascii-magic](https://pypi.org/project/ascii-magic/), then display each frame to the terminal using [list2term](https://pypi.org/project/list2term/).

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

Use `ascii-art-animator` to convert the following GIF image to an ascii animation and demonstrate the use of the optional arguments.
* show x and y axis
* loop through the image 3 times 
* set columns to 100 characters

```bash
ascii-art-animator -f docs/images/marcovich.gif -a -m 3 -c 100
```
**GIF Input**

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich.gif)

**Program Output**

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich-exec.gif)

---

### The `Animation` class ⭐

Use the Animation class to create your own animations.

#### [Binary Search Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example5.py)

A binary search is a search algorithm that finds a specific value in a sorted array by repeatedly dividing the search interval in half.

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example5.gif)

#### [Selection Sort Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example4.py)

A selection sort search is a simple and efficient sorting algorithm that works by repeatedly selecting the smallest (or largest) element from the unsorted portion of the list and moving it to the sorted portion of the list.

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example4.gif)

Here is another [example](https://github.com/soda480/ascii-animator/blob/main/examples/example6.py) of a selection sort animation this time using vertical bars.

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example6.gif)

#### [Equalizer Bars Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example2.py)

An animation for symmetrical equalizer bars.

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example2.gif)

#### [Matrix Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example3.py)

A Matrix animation.

![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example3.gif)

#### [Game-Of-Life](https://github.com/soda480/game-of-life)

A Conway Game-Of-Life implementation that uses `ascii_animator` to display the game to the terminal.

---

### Installation 🚀

Clone the repository and ensure the latest version of Docker is installed on your development server.

1) Build the Docker image:
```bash
docker image build \
-t ascii-animator:latest .
```

2) Run the Docker container:
```bash
docker container run \
--rm \
-it \
-v $PWD:/code \

ascii-animator:latest \
bash
```

3) Execute the build:
```sh
pyb -X
```

---

### 📄 Issues & Support  

Encounter a problem? Have a suggestion? Feel free to **open an issue** and include the following details:  

- ✅ **Clear description** of the issue or feature request  
- 🛠️ **Steps to reproduce** (if applicable)  
- 📸 **Screenshots or logs** (if relevant)  
- 💡 **Expected vs. actual behavior**  

Your feedback helps improve the project—thank you for contributing! 🚀  



