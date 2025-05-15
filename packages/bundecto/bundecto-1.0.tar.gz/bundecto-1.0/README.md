# bundecto

**bundecto** is a minimal terminal-based text editor written in Python using `curses`. It aims to provide a distraction-free, keyboard-only editing experience directly in your terminal.

## Features

- Minimal interface with a focus on productivity
- Fully keyboard-driven controls
- Support for scrolling, cursor movement, and text editing
- Quick save to file with Ctrl+S
- Exit with Ctrl+X
- Ctrl+H to show keybind help menu
- Ctrl+G to open debug menu

## Installation

You can install `bundecto` using `pip`:

```bash
pip install bundecto
```

Or install from source:

```bash
git clone https://github.com/voyager-2021/bundecto.git
cd bundecto
pip install .
```

## Usage

Launch the editor from your terminal:

```bash
bund [filename] [-v|-h|-r]
```

If the file exists, it will be loaded. Otherwise, a new buffer is created.

## Development

Clone the repo and install in editable mode:

```bash
git clone https://github.com/voyager-2021/bundecto.git
cd bundecto
pip install -e .
```

## Bug Reporting

If you encounter any bugs, please help us improve **bundecto** by reporting issues on the GitHub repository:

- Check if the issue is already reported before opening a new one.
- Provide clear steps to reproduce the bug.
- Include your operating system, Python version, and terminal emulator details.
- If possible, include error messages or screenshots.

Report bugs to: [bundecto/issues](https://github.com/voyager-2021/bundecto/issues)

## License

This project is licensed under the MIT License.

## Acknowledgments

Inspired by the elegance of modal and minimal editors like `micro`, `nano`, and `pico`, but aimed to be as simple as possible in pure Python.
