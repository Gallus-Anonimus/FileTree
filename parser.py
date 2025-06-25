import argparse
import configparser
import os
import sys
from colors import Color
from utils import prompt_list, prompt_int


def load_config(config_file_path: str = 'config.ini') -> dict:
    config_parser = configparser.ConfigParser()
    config_data = {}

    if os.path.exists(config_file_path):
        try:
            config_parser.read(config_file_path)
            if 'GENERAL' in config_parser and 'path' in config_parser['GENERAL']:
                config_data['path'] = config_parser['GENERAL']['path']

            if 'FILTERS' in config_parser:
                if 'include_extensions' in config_parser['FILTERS']:
                    config_data['include_extensions'] = [
                        ext.strip() for ext in config_parser['FILTERS']['include_extensions'].split(',') if ext.strip()
                    ]
                if 'exclude_names' in config_parser['FILTERS']:
                    config_data['exclude_names'] = [
                        name.strip() for name in config_parser['FILTERS']['exclude_names'].split(',') if name.strip()
                    ]
                if 'exclude_prefixes' in config_parser['FILTERS']:
                    config_data['exclude_prefixes'] = [
                        p.strip() for p in config_parser['FILTERS']['exclude_prefixes'].split(',') if p.strip()
                    ]

            if 'DISPLAY' in config_parser and 'max_depth' in config_parser['DISPLAY']:
                try:
                    depth = config_parser.getint('DISPLAY', 'max_depth')
                    config_data['max_depth'] = depth if depth != -1 else None
                except ValueError:
                    print(f"Warning: Invalid 'max_depth' value", file=sys.stderr)

        except Exception as e:
            print(f"Error loading config: {e}", file=sys.stderr)

    return config_data


def parse_arguments_and_config() -> dict:
    parser = argparse.ArgumentParser(description="Directory tree viewer with filters and colors.")
    parser.add_argument("path", nargs="?", default=None)
    parser.add_argument("-i", "--include", type=str, default="")
    parser.add_argument("-e", "--exclude", type=str, default="")
    parser.add_argument("-ep", "--exclude-prefixes", type=str, default="")
    parser.add_argument("-d", "--depth", type=int, default=None)

    args = parser.parse_args()
    config_data = load_config()

    cli_provided = any([args.path, args.include, args.exclude, args.exclude_prefixes, args.depth is not None])
    config_loaded = bool(config_data)
    prompt_user = not cli_provided and not config_loaded

    settings = {
        'path': args.path or config_data.get('path'),
        'include_extensions': args.include.split(",") if args.include else config_data.get('include_extensions', []),
        'exclude_names': args.exclude.split(",") if args.exclude else config_data.get('exclude_names', []),
        'exclude_prefixes': args.exclude_prefixes.split(",") if args.exclude_prefixes else config_data.get('exclude_prefixes', []),
        'max_depth': args.depth if args.depth is not None else config_data.get('max_depth')
    }

    # Prompt only in full manual fallback
    if prompt_user:
        p = input("Enter directory path (leave empty for current): ").strip()
        settings['path'] = p if p else '.'

        exts = prompt_list("Enter file extensions to include (comma separated, leave empty for all): ")
        if exts:
            settings['include_extensions'] = exts

        names = prompt_list("Enter file/folder names to exclude (comma separated, leave empty for none): ")
        if names:
            settings['exclude_names'] = names

        prefixes = prompt_list("Enter prefixes to exclude (comma separated, leave empty for none): ")
        if prefixes:
            settings['exclude_prefixes'] = prefixes

        depth = prompt_int("Enter maximum directory depth (number, leave empty for no limit): ", default_value=None)
        if depth is not None:
            settings['max_depth'] = depth

    return settings

def write_config(path=None, include=None, exclude=None, prefixes=None, depth=None, config_file="config.ini"):
    config = configparser.ConfigParser()

    config["GENERAL"] = {}
    if path is not None:
        config["GENERAL"]["path"] = path

    config["FILTERS"] = {}
    if include is not None:
        config["FILTERS"]["include_extensions"] = ",".join(include)
    if exclude is not None:
        config["FILTERS"]["exclude_names"] = ",".join(exclude)
    if prefixes is not None:
        config["FILTERS"]["exclude_prefixes"] = ",".join(prefixes)

    config["DISPLAY"] = {}
    if depth is not None:
        config["DISPLAY"]["max_depth"] = str(depth)

    try:
        with open(config_file, "w") as f:
            config.write(f)
        print(f"Configuration saved to {config_file}")
    except Exception as e:
        print(f"\033[91m Failed to write config: {e}", file=sys.stderr)


def show_config(config_file_path="config.ini"):
    if not os.path.exists(config_file_path):
        print(f"No config file found at {config_file_path}")
        return

    config = configparser.ConfigParser()
    try:
        config.read(config_file_path)
        print(f" Current configuration from {config_file_path}:\n")
        for section in config.sections():
            print(f"[{section}]")
            for key, value in config[section].items():
                print(f"{key} = {value}")
            print()
    except Exception as e:
        print(f"Error reading config file: {e}", file=sys.stderr)
