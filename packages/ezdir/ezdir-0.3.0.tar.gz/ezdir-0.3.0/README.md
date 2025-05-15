# ezdir

Simple utilities to change the current working directory in Python:

- `up(n)` changes working folder to be up `n` directory levels.
- `goto("foldername")` changes working folder to the first parent folder (within the original path) matching a name.
- `find("foldername")` changes working folder to the first parent folder matching a name under `n` directory levels.

## Examples

If your current file is `Users/me/MyWork/src/main/work[.py/.ipynb]` and you wanted to
go up one level to `src` you could use the `up` function:

```python
import ezdir

ezdir.up(levels=1)
```

If you wanted to go to `Users/me/MyWork/src` you could go up two levels or use the `goto` function:

```python
import ezdir

ezdir.trim(folder_name='src')
```

As the `src` folder is within the original path.

If you wanted to switch your working directory to `Users/me/MyWork/tests` you could use `find`:

```python
import ezdir

ezdir.find(levels=2, folder_name='tests')
```

As this will go `up` two levels, and then search for a `tests` folder. We include a number
of excluded folders (e.g. `build`), but you can exclude more folders by passing a list to
the `ezdir.find` as the `add_ignore_subfolders` variable.

## Installation

```bash
pip install ezdir
```

## Why use it?

### Changing working directory in a Jupyter Notebook

If you are using a notebook on a cloud server, your working directory might
be different to some elses. Normally people do something like:

```python
import os

os.chdir(path)
```

But sometimes this path will be different based on the user. This library provides
a more sensible way of going up folder paths whether you're using a python script or
a notebook.

