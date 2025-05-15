#!/bin/env python3
from pathlib import Path
import json
import sys,os
from openai import OpenAI
from rich.console import Console
console=Console()

here = os.path.abspath(os.path.dirname(__file__))

def app_dir():
    with open(Path("~/.gairc").expanduser(), "r") as file:
        rc=file.read()
        jsoned = json.loads(rc)
        return Path(jsoned["app_dir"]).expanduser()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Gai CLI Tool')
    parser.add_argument('command', choices=['init', 'pull'], help='Command to run')
    parser.add_argument('-f', '--force', action='store_true', help='Force initialization')
    parser.add_argument('extra_args', nargs='*', help='Additional arguments for commands')
    parser.add_argument("--repo-name", default="kakkoii1337", help="Repository name for Docker image.")
    parser.add_argument("--image-name", help="Base name for Docker image, which is required.")
    parser.add_argument("--dockerfile-path", default="./Dockerfile", help="Path to the Dockerfile used for building the image.")
    parser.add_argument("--dockercontext-path", default=".", help="Path to the Dockerfile used for building the image.")
    parser.add_argument("--no-cache", action="store_true", help="Do not use cache when building the image.")

    args = parser.parse_args()

    if args.command == "init":
        from gai.scripts.gai_init import init
        print("Initializing...by force" if args.force else "Initializing...")
        init(force=args.force)
    elif args.command == "pull":
        if args.extra_args:
            from gai.scripts.gai_pull import pull
            pull(console, args.extra_args[0])
        else:
            console.print("[red]Model name not provided[/]")
    else:
        console.print("[red]Invalid command[/]")

if __name__ == "__main__":
    main()
