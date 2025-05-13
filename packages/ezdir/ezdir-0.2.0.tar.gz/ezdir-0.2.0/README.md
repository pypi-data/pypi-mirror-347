# ezdir

Simple utilities to change the current working directory in Python:

- `up(n)` changes working folder to be up `n` directory levels.
- `find("foldername")` changes working folder to the first parent folder matching a name.

## Installation

```bash
pip install ezdir
```

## Example

```python
import ezdir

ezdir.up(1) # Change current working directory to one level up
ezdir.find("GitProjects") # Change current working directory to a parent folder named 'GitProjects'
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

