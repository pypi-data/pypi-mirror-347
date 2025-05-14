import pathlib
import os
import subprocess

from .build_tools import get_build_directory

def run(path: pathlib.Path, args: list[str]) -> int:
    """
    Run a command from within the built environment.
    """

    venv_path = path / ".venv"
    bin_path = venv_path / "Scripts" if os.name == "nt" else venv_path / "bin"

    activate_path = bin_path / "activate.bat" if os.name == "nt" else bin_path / "activate"

    execution = subprocess.run(
        [activate_path, "&&"] + args,
        shell=True,
        check=True,
        cwd=get_build_directory(path),
        env=os.environ.copy(),
    )

    return execution.returncode

run(pathlib.Path(__file__).parent, ["python", "--version"])