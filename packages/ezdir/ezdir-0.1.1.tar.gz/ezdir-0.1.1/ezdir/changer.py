import os
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def parent():
    """
    Returns the full path of the file or notebook that called this function.
    Works in Jupyter notebooks too.
    """
    try:
        # Jupyter notebook
        from IPython import get_ipython
        ipython = get_ipython()
        if ipython and hasattr(ipython, 'run_line_magic'):
            return os.path.abspath(ipython.starting_dir)
    except Exception:
        pass

    # Inspect the call stack and get the caller's file path
    frame_depth = 2  # Default depth to look back
    try:
        # Check if the stack has enough frames
        frame = sys._getframe(frame_depth)
    except ValueError:
        # If not enough frames, adjust depth to 1
        frame_depth = 1
        frame = sys._getframe(frame_depth)

    filename = frame.f_globals.get('__file__', None)
    if filename:
        return os.path.dirname(filename)
    

def up(levels=1):
    """
    Get the path of the file or notebook and go up a number of levels.
    Changes the working directory.

    Parameters:
    - levels (int): number of levels to go up

    Returns:
    - str: new current directory
    """
    if levels < 1:
        raise ValueError("levels must be >= 1")

    start_path = parent()
    for _ in range(levels):
        start_path = os.path.dirname(start_path)

    os.chdir(start_path)
    logger.info(f"Changed to {start_path}")
    return start_path

def find(folder_name):
    """
    Searches up from the current file's path for a parent folder with the given name.
    Changes to it if found.

    Parameters:
    - folder_name (str): name of the folder to find

    Returns:
    - str: new current directory

    Raises:
    - FileNotFoundError: if folder is not found
    """
    path = os.path.dirname(parent())

    while True:
        if os.path.basename(path) == folder_name:
            os.chdir(path)
            logger.info(f"Changed to {path}")
            return path

        parent = os.path.dirname(path)
        if parent == path:
            raise FileNotFoundError(f"Folder '{folder_name}' not found.")
        path = parent
        
