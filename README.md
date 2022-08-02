# Results-py

Rust-like Monadic results in Python

## TODO

- [x] Add a test suite
- [ ] Make an installable package
- [ ] Docs and examples

## Example

```python
import typing
from results import Ok, Err

Result = t.Union[Ok, Err]

def func_that_fails() -> Result:
    return Err("Error")

def func_that_succeeds() -> Result:
    return Ok(42)

func_that_succeeds().is_ok()  # True
func_that_fails().is_ok()     # False

func_that_succeeds().unwrap() # 42
func_that_fails().unwrap()    # Crashes here
```
