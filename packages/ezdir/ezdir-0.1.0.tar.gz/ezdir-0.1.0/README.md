# ezdir

Simple utilities to change the current working directory in Python:

- `up(n)` goes up `n` directory levels.
- `find("foldername")` goes up to the first parent folder matching a name.

## Installation

```bash
pip install -e .

## Example

```python
from updir import up, find

up(2)               # Go up two levels
find("scripts")     # Change to a parent folder named 'scripts'
```
