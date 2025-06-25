# FileTree

A Python script to display directory contents in a tree-like format with advanced, file-type-based coloring.  
Supports filtering by file extensions, excluding specific files/folders or prefixes, and limiting directory depth.

---

## Features

- Color-coded output based on file types and extensions (e.g., Python, JavaScript, images, archives, executables).
- Filter files by extensions to include.
- Exclude specific files or folders by name or prefix.
- Limit the depth of directory traversal.
- Interactive prompts if no command-line arguments are provided.
- Handles permission errors gracefully.

---

## Installation

No external dependencies required.  
Requires Python 3.11+.

Clone or download this repository and run the script directly:

Run directly with Python:

```bash
python main.py
```

Or run the batch file on Windows:

```bash
FileTree.bat
```

Or after adding to your PATH, simply:

```bash
FileTree
```

---

## Usage

```bash
FileTree [path] [options]
```

### Arguments

- `path` (optional): Directory path to list. If omitted, the script will prompt for input.

### Options

- `-h`, `--help`  
  Shows help menu explaining all available commands.
  Show help menu explaining all available commands.

- `--config`  
  Modify the `config.ini` instead of displaying the tree. Use flags to save settings.

- `--show-config`  
  Show current config and exit.

- `-i`, `--include`  
  Comma-separated list of file extensions to include (e.g., `py,txt,md`).  
  If empty, all files are included.

- `-e`, `--exclude`  
  Comma-separated list of file or folder names to exclude (e.g., `.git,node_modules`).

- `-ep`, `--exclude-prefixes`  
  Comma-separated list of prefixes to exclude (e.g., `__pycache__,.DS_Store`).

- `-d`, `--depth`  
  Maximum directory depth to display (e.g., `2` for two levels).  
  Use `0` to show only the current directory. Leave empty for no limit.

---

## Examples

List the current directory with all files:

```bash
FileTree
```

List `/home/user/projects` including only Python and Markdown files, excluding `.git` folder, up to 3 levels deep:

```bash
FileTree /home/user/projects -i py,md -e .git -d 3
```

Exclude files/folders starting with `temp` or `.cache` prefixes:

```bash
FileTree /path/to/dir -ep temp,.cache
```

---

## Color Legend

| File Type            | Color Example         |
|----------------------|-----------------------|
| Python               | Blue                  |
| C/C++                | Cyan                  |
| Java                 | Red                   |
| JavaScript           | Yellow                |
| Go                   | Green                 |
| Rust                 | Orange                |
| Ruby                 | Magenta               |
| PHP                  | Pink                  |
| HTML                 | Orange-Red            |
| CSS                  | Dark Blue             |
| Text/Markdown/Log    | White / Magenta       |
| JSON/YAML            | Orange                |
| XML/Config           | Gray                  |
| CSV                  | Light Green           |
| Executables/Binaries | Red                   |
| Archives             | Brownish              |
| Images               | Purple                |
| Audio                | Light Purple          |
| Video                | Dark Purple           |
| Directories          | White                 |

---

## Notes

- The script uses ANSI escape codes for coloring, so it works best in terminals that support ANSI colors.
- Executable detection is based on file extensions and executable permission bits.
- Permission errors when accessing directories are caught and displayed as `[Permission Denied]`.

---

## Config Edition

Example of `config.ini`:

```ini
[GENERAL]
path = .

[FILTERS]
include_extensions = py,txt,md
exclude_names = __pycache__
exclude_prefixes = _,.

[DISPLAY]
max_depth = 3
```

### How to edit

There are two ways to edit the config:

- Directly edit the `config.ini` file (example above).
- Use command-line flags with the `--config` option to save settings. Remember is you want do edit `config.ini` by flags provide all constrains you want to have `confing.ini` is being recreated without taking in consideration curent `config.ini` 

---
