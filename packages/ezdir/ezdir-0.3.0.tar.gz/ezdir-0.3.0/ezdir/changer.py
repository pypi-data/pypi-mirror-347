import os
import sys
import logging
from ezdir.util.system_folders import ignore_subfolders

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

def up(levels=1, change=True):
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

    if change:
        os.chdir(start_path)
        logger.info(f"Changed to {start_path}")
    return start_path

def goto(folder_name):
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

        parent_path = os.path.dirname(path)  # Renamed to avoid conflict
        if parent_path == path:
            raise FileNotFoundError(f"Folder '{folder_name}' not found.")
        path = parent_path
  

def find(levels, folder_name, add_ignore_subfolders=None):
    """
    Searches within subfolders from a specified parent folder (using `up`)
    for a parent folder with the given name. Changes to it if found.

    Parameters:
    - levels (int): number of levels to go up
    - folder_name (str): name of the folder to find

    Returns:
    - str: new current directory

    Raises:
    - FileNotFoundError: if folder is not found
    """
    if type(add_ignore_subfolders) is list and add_ignore_subfolders is not None:
        igsf = ignore_subfolders + add_ignore_subfolders
    else:
        igsf = ignore_subfolders

    folder_found = False

    for root, dirs, _ in os.walk(up(levels, change = False), topdown=False):
        for name in dirs:
            path = os.path.join(root, name)
            if os.path.basename(path) == folder_name:
                if any(i in path for i in igsf):
                    None
                else:
                    os.chdir(path)
                    logger.info(f"Changed to {path}")
                    folder_found = True

    if folder_found == False:
        raise FileNotFoundError(f"Folder '{folder_name}' not found.")
  