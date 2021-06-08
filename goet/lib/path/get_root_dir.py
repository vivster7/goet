from pathlib import Path

ROOT_DIR_NAME = 'goet'

def get_root_dir(filepath: str) -> Path:
    """Computes root directory from any file.
    
    >>> get_root_dir()
    '/Users/vivek.dasari/Code/goet'
    """
    if ROOT_DIR_NAME not in filepath:
        raise ValueError(f"Cannot find {ROOT_DIR_NAME} in {filepath}")

    relpath = filepath[filepath.index(ROOT_DIR_NAME):]
    count = relpath.count('/')
    return Path(filepath).joinpath('/'.join(['..'] * count)).resolve()
