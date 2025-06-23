import os
import sys
import argparse


class Color:
    # Directories
    WHITE= '\033[97m'

    # Programming Languages
    PYTHON = '\033[94m'   # Python
    C_CPP = '\033[96m'    # C/C++
    JAVA = '\033[91m'     # Java
    JAVASCRIPT = '\033[93m' # JavaScript
    GO = '\033[92m'       # Go
    RUST = '\033[38;5;208m' # Rust
    RUBY = '\033[95m'     # Ruby
    PHP = '\033[38;5;165m' # PHP
    HTML = '\033[38;5;202m' # HTML
    CSS = '\033[38;5;27m'  # CSS

    # Text and Data Files
    TEXT = '\033[97m'     # Generic text files
    MARKDOWN = '\033[95m' # Markdown
    JSON = '\033[38;5;208m' # JSON
    YAML = '\033[38;5;208m' # YAML
    XML = '\033[38;5;242m'  # XML
    CSV = '\033[38;5;107m'  # CSV

    # Executables and Binaries
    EXECUTABLE = '\033[91m' # Executable files
    ARCHIVE = '\033[38;5;172m' # Archive files

    # Images and Media
    IMAGE = '\033[38;5;128m' # Image
    AUDIO = '\033[38;5;105m' # Audio
    VIDEO = '\033[38;5;93m'  # Video

    # Configuration Files
    CONFIG = '\033[38;5;242m' # Configuration

    DEFAULT_FILE = '\033[92m'

    RESET = '\033[0m'


total_dirs = 0
total_files = 0

def get_file_color(filename: str) -> str:
    """Returns the ANSI escape code for the color based on file extension."""
    lower_filename = filename.lower()
    _, ext = os.path.splitext(lower_filename)

    # Programming Languages
    if ext in ('.py', '.pyc', '.pyo'):
        return Color.PYTHON
    elif ext in ('.c', '.cpp', '.h', '.hpp'):
        return Color.C_CPP
    elif ext == '.java':
        return Color.JAVA
    elif ext in ('.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'):
        return Color.JAVASCRIPT
    elif ext == '.go':
        return Color.GO
    elif ext == '.rs':
        return Color.RUST
    elif ext in ('.rb', '.rake'):
        return Color.RUBY
    elif ext in ('.php', '.phtml'):
        return Color.PHP
    elif ext in ('.html', '.htm'):
        return Color.HTML
    elif ext == '.css':
        return Color.CSS
    elif ext in ('.sh', '.bash', '.zsh', '.ps1'):
        return Color.EXECUTABLE

    # Text and Data Files
    elif ext == '.txt':
        return Color.TEXT
    elif ext in ('.md', '.markdown'):
        return Color.MARKDOWN
    elif ext == '.json':
        return Color.JSON
    elif ext in ('.yml', '.yaml'):
        return Color.YAML
    elif ext == '.xml':
        return Color.XML
    elif ext == '.csv':
        return Color.CSV
    elif ext == '.log':
        return Color.TEXT

    # Executables and Binaries
    elif os.access(os.path.join(os.path.dirname(__file__), filename), os.X_OK):
        return Color.EXECUTABLE
    elif ext in ('.exe', '.bin', '.dll', '.so', '.dylib'):
        return Color.EXECUTABLE

    # Archive files
    elif ext in ('.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z'):
        return Color.ARCHIVE

    # Images
    elif ext in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'):
        return Color.IMAGE

    # Audio
    elif ext in ('.mp3', '.wav', '.ogg', '.flac', '.aac'):
        return Color.AUDIO

    # Video
    elif ext in ('.mp4', '.mkv', '.avi', '.mov', '.webm'):
        return Color.VIDEO

    # Configuration Files (generic)
    elif ext in ('.conf', '.ini', '.cfg'):
        return Color.CONFIG



    else:
        return Color.DEFAULT_FILE

def tree(path: str, extensions: list[str], exclude: list[str], exclude_prefixes: list[str],
         max_depth: int | None, current_depth: int, prefix="") -> None:
    global total_dirs, total_files

    if max_depth is not None and current_depth >= max_depth:
        return

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        print(prefix + "[Permission Denied]")
        return

    entries = [e for e in entries if e not in exclude and not any(e.startswith(p) for p in exclude_prefixes)]
    entries_count = len(entries)

    for index, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            if extensions and not any(entry.endswith(ext) for ext in extensions):
                continue
            total_files += 1
            color = get_file_color(entry)
        else:
            total_dirs += 1
            color = Color.WHITE # Directories remain white
        connector = "├── " if index < entries_count - 1 else "└── "
        print(prefix + connector + f"{color}{entry}{Color.RESET}")

        if os.path.isdir(full_path):
            extension_prefix = "│   " if index < entries_count - 1 else "    "
            if max_depth is None or (current_depth + 1) < max_depth:
                 tree(full_path, extensions, exclude, exclude_prefixes,
                      max_depth, current_depth + 1, prefix + extension_prefix)



def prompt_list(prompt_text: str) -> list[str]:
    user_input = input(prompt_text).replace(" ", "")
    return user_input.split(",") if user_input else []

def prompt_int(prompt_text: str, default_value: int | None = None) -> int | None:
    while True:
        user_input = input(prompt_text).strip()
        if not user_input:
            return default_value
        try:
            value = int(user_input)
            if value >= 0:
                return value
            else:
                print("Please enter a non-negative number for depth.")
        except ValueError:
            print("Invalid input. Please enter a number or leave empty.")


def main():
    parser = argparse.ArgumentParser(description="Lists directory contents in a tree-like format with advanced coloring.")
    parser.add_argument("path", nargs="?", default=None, help="Path to the directory to list (optional).")
    parser.add_argument("-i","--include", type=str, default="", help="Comma-separated file extensions to include (e.g., 'py,txt')." )
    parser.add_argument("-e","--exclude", type=str, default="", help="Comma-separated file/folder names to exclude (e.g., '.git,node_modules')." )
    parser.add_argument("-ep","--exclude-prefixes", type=str, default="", help="Comma-separated prefixes to exclude (e.g., '__pycache__,.DS_Store')." )
    parser.add_argument("-d","--depth", type=int, default=None, help="Maximum directory depth to display (e.g., 2 for two levels deep). Use 0 for just the current directory.")

    args = parser.parse_args()

    path = None
    extensions = []
    exclude = []
    exclude_prefixes = []
    max_depth = None

    if args.path is None:
        path = input("Enter path to the directory: ").strip()
        extensions = prompt_list("Enter file extensions to include (comma separated, leave empty for all): ")
        exclude = prompt_list("Enter file/folder names to exclude (comma separated, leave empty for none): ")
        exclude_prefixes = prompt_list("Enter prefixes to exclude (comma separated, leave empty for none): ")
        max_depth = prompt_int("Enter maximum directory depth (number, leave empty for no limit): ",default_value=None)
    else:
        path = args.path
        extensions = args.include.split(",") if args.include else []
        exclude = args.exclude.split(",") if args.exclude else []
        exclude_prefixes = args.exclude_prefixes.split(",") if args.exclude_prefixes else []
        max_depth = args.depth

    if not os.path.exists(path) or not os.path.isdir(path):
        print(f"Error: Invalid directory path: '{path}'")
        return

    print(f"\n{Color.WHITE}{path}{Color.RESET}") # Color the root path
    tree(path, extensions, exclude, exclude_prefixes, max_depth, 0)
    print()

    print(f"Total directories: {total_dirs}")
    print(f"Total files: {total_files}")


if __name__ == "__main__":
    main()
