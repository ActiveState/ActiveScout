import os
import platform
from typing import Iterator, List, Optional


def dirwalker() -> Iterator[str]:
    """
    Returns a generator with most/all files on a system's main drive.
    """
    toplevel_dir: str = ""
    toplevel_include: Optional[List] = None
    for dirpath, dirs, files in os.walk("/", topdown=True, followlinks=False):
        if platform.system() == "Linux" or platform.system() == "Darwin":
            toplevel_dir = "/"
            # on Linux, prune most root level directories
            toplevel_include = [
                "bin",
                "lib",
                "etc",
                "opt",
                "usr",
                "home",
                # macos home
                "Users",
            ]
        elif platform.system() == "Windows":
            toplevel_dir = "C:/"

    for dirpath, dirs, files in os.walk(toplevel_dir, topdown=True, followlinks=False):
        if toplevel_include and dirpath == toplevel_dir:
            dirs[:] = [d for d in dirs if d in toplevel_include]
        for file in files:
            yield f"{dirpath}/{file}"
