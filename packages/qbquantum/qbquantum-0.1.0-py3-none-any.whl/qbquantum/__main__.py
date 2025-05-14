import sys
from pathlib import Path

from qbquantum.building import build_project
from qbquantum.initializing import init
from qbquantum.managing import install_dependencies, modify, Action, get_dependencies

def main(args=None):
    if args is None:
        args = sys.argv[1:] or ["help"]

    command = args[0]

    cwd = Path.cwd()

    match command:
        case "init":
            path = Path(args[1]) if len(args) > 1 else None
            init(path)

        case "help":
            commands = {
                "init": "Initialize a new quantum project.",
                "install": "Install dependencies.",
                "add": "Add packages to the qbproject.toml file.",
                "remove": "Remove packages from the qbproject.toml file.",
                "list": "List all dependencies in the qbproject.toml file.",
            }

            print("Available commands:")
            for cmd, desc in commands.items():
                print(f"  {cmd}: {desc}")
            return

        case "install":
            install_dependencies(cwd)

        case "add":
            packages = args[1:] if len(args) > 1 else None

            if not len(packages):
                print("Please provide a package name.")
                return

            modify(cwd, packages, Action.ADD)
            install_dependencies(cwd)

        case "remove":
            packages = args[1:] if len(args) > 1 else None

            if not len(packages):
                print("Please provide a package name.")
                return

            modify(cwd, packages, Action.REMOVE)
            install_dependencies(cwd)

        case "list":
            dependencies = get_dependencies(cwd)

            if dependencies:
                print("Installed packages:")
                for dep in dependencies:
                    print(f"  - {dep}")

            else:
                print("No dependencies found.")
                return

        case "build":
            clean = "clean" in args[1:]
            build_project(cwd, clean)