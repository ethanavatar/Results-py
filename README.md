# Results-py

Rust-like Monadic results in Python

## TODO

- [x] Add a test suite
- [x] Make an installable package
- [ ] Docs and examples

## Example

```python
from __future__ import annotations
import typing as t
from results import Ok, Err, Result, UnwrapError

def divide_checked(dividend: int, divisor: int) -> Result[int, str]:
    if divisor == 0:
        return Err("Cannot divide by zero")
    return Ok(dividend / divisor)

assert divide_checked(4, 2).unwrap_or(0) == 2
assert divide_checked(1, 0).unwrap_or(-42) == -42
try:
    divide_checked(1, 0).expect("This should not happen")
except UnwrapError as e:
    print(e) # prints: "This should not happen"
```
