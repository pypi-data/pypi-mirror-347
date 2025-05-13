# ezdir

Simple utilities to change the current working directory in Python:

- `up(n)` goes up `n` directory levels.
- `find("foldername")` goes up to the first parent folder matching a name.

## Installation

```bash
pip install ezdir
```

## Example

```python
import ezdir

ezdir.up(2)               # Go up two levels
ezdir.find("scripts")     # Change to a parent folder named 'scripts', errors if it doesn't exist
```
