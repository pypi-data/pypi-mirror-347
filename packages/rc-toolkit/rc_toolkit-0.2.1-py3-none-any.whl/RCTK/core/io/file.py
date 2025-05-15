from os import path, makedirs
from pathlib import Path

from ..env import is_debug

from typing import NoReturn

def mkdir(file_path: str) -> NoReturn:
    """
    make file dirs

    Args:
        file_path (str): file path
    """
    dir_path = Path(file_path).parent
    if path.isdir(dir_path): return
    try: makedirs(dir_path)
    except Exception:  # pylint: disable=broad-exception-caught
        if not is_debug(): return  
        raise

def get_name(path: str) -> tuple:
    f_path = Path(path)
    return [f_path.stem, f_path.suffix]
