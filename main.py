import argparse
import os
import sys
from colors import Color
from parser import parse_arguments_and_config, write_config,show_config

total_dirs = 0
total_files = 0


def tree(path, extensions, exclude, exclude_prefixes, max_depth, current_depth=0, prefix=""):
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
        connector = "├── " if index < entries_count - 1 else "└── "

        if os.path.isdir(full_path):
            total_dirs += 1
            print(prefix + connector + f"{Color.WHITE}{entry}{Color.RESET}")
            extension_prefix = "│   " if index < entries_count - 1 else "    "
            tree(full_path, extensions, exclude, exclude_prefixes, max_depth, current_depth + 1, prefix + extension_prefix)

        elif os.path.isfile(full_path):
            if extensions and not any(entry.endswith(ext) for ext in extensions):
                continue
            total_files += 1
            color = Color.get_file_color(entry)
            print(prefix + connector + f"{color}{entry}{Color.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Directory tree viewer with filters and config support.")
    parser.add_argument("--config", action="store_true", help="Modify the config.ini instead of displaying the tree")
    parser.add_argument("--show-config", action="store_true", help="Show current config and exit")
    parser.add_argument("--path", type=str)
    parser.add_argument("-i", "--include", type=str)
    parser.add_argument("-e", "--exclude", type=str)
    parser.add_argument("-ep", "--exclude-prefixes", type=str)
    parser.add_argument("-d", "--depth", type=int)


    args = parser.parse_args()

    if args.show_config:
        show_config()
        return

    if args.config:
        write_config(
            path=args.path,
            include=args.include.split(",") if args.include else None,
            exclude=args.exclude.split(",") if args.exclude else None,
            prefixes=args.exclude_prefixes.split(",") if args.exclude_prefixes else None,
            depth=args.depth
        )
        return

    # Show tree view
    settings = parse_arguments_and_config()

    if not settings['path']:
        print("Error: No path provided.", file=sys.stderr)
        return

    if not os.path.exists(settings['path']) or not os.path.isdir(settings['path']):
        print(f"Error: Invalid directory path: '{settings['path']}'", file=sys.stderr)
        return

    print(f"\n{Color.WHITE}{settings['path']}{Color.RESET}")
    tree(
        settings['path'],
        settings['include_extensions'],
        settings['exclude_names'],
        settings['exclude_prefixes'],
        settings['max_depth']
    )
    print()
    print(f"Total directories: {total_dirs}")
    print(f"Total files: {total_files}")


if __name__ == "__main__":
    main()
