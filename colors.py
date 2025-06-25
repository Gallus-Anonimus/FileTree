import os
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
