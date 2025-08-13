# Contributing

## Information

This project uses [Pyodide](https://pyodide.org) to run Python directly in the browser using WebAssembly (WASM).  
Almost no JavaScript is required — the frontend is written entirely in Python and HTML/CSS.

## Dev Code Checks

Use `ruff check` to check your code style. and fix it

```shell
ruff check .
ruff check . --fix
```

Use `pre-commit` to run linting before committing. `pre-commit install` to install.

### Examples

```shell
pre-commit run --show-diff-on-failure --all-files
pre-commit run ruff-check --all-files
pre-commit run check-toml --all-files
```

**Pre-commit hooks:**

- `check-toml`: Lints and corrects your TOML files.
- `check-yaml`: Lints and corrects your YAML files.
- `end-of-file-fixer`: Makes sure you always have an empty line at the end of your file.
- `trailing-whitespace`: Removes whitespaces at the end of each line.
- `ruff-check`: Runs the Ruff linter.
- `ruff-format`: Runs the Ruff formatter.

## Our coding rules

1. Comment your classes, functions, and non-obvious logic.
2. Use docstrings with author tags and short descriptions.

```py
class ClassName:
    '''Handle user input and validation.

    @author Mira
    '''
    ...

# Short function description
def do_something():
    '''Perform a single-step operation.

    :param paramname: does something
    :return: None

    @author Mira
    '''
    ...
```

## Naming Stuff Rules

Use `ruff check` to check your code style. and fix it

```shell
ruff check .
ruff check . --fix
```

**Functions**: lowercase and use underscores

```py
def my_function():
    my_variable = "value"
```

**Classes and Variable names**: PascalCase style

```py
from typing import List

class MyClass:
    pass

ListOfMyClass = List[MyClass]
```

**Constants**: SCREAMING_SNAKE_CASE style

```py
MY_CONSTANT = 1
```

**Operators**: at the start of a newline

```py
# No
result = (
    1 +
    2 *
    3
)
# Yes
result = (
    1
    + 2
    * 3
)
```

**equivalent to None**: use `is`, `is not` instead of `==`

```py
if variable == None: # No
    print("Variable is None")
if variable is None: # Yes
    print("Variable is None")¨
```

**not** positioning:

```py
if not variable is None: # No
    print("Variable is not None")

if variable is not None: # Yes, easier to read
    print("Variable is not None")
```

**Imports**: do not import multiple modules on one line or everything from a module (\*)

```py
# No
import pathlib, os
from pathlib import *

# Yes
import os
import pathlib
from pathlib import Path
```
