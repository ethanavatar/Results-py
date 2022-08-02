from __future__ import annotations
import typing as t

class UnwrapError(Exception):
    pass

class _Result:
    def __init__(self, value: t.Any, is_ok: bool):
        self._value = value

        self._ok = is_ok

    def is_ok(self) -> bool:
        return self._ok

    def is_err(self) -> bool:
        return not self._ok

    def expect_err(self, msg: str) -> t.Any:
        if self.is_ok():
            raise UnwrapError(msg)
        else:
            return self._value

    def expect(self, msg: str) -> t.Any:
        if self.is_ok():
            return self._value
        else:
            raise UnwrapError(msg)

    def unwrap(self) -> t.Any:
        if self.is_ok():
            return self._value
        else:
            raise UnwrapError(f"unwrap called on Err: {self._value}")

    def unwrap_err(self) -> t.Any:
        if self.is_ok():
            raise UnwrapError(f"unwrap_err called on Ok: {self._value}")
        else:
            return self._value

    def unwrap_unchecked(self) -> t.Any:
        return self._value

    def And(self, res: Result) -> Result:
        if self.is_ok():
            if res.is_ok():
                return res
            else:
                return Err(res._value)
        else:
            return self

    def And_then(self, op: t.Callable[[t.Any], Result]) -> Result:
        if self.is_ok():
            return op(self._value)
        else:
            return self

    def Or(self, res: Result) -> Result:
        if self.is_ok():
            return self
        else:
            return res

    def Or_else(self, op: t.Callable[[t.Any], Result]) -> Result:
        if self.is_ok():
            return self
        else:
            return op(self._value)

    def unwrap_or(self, default: t.Any) -> t.Any:
        if self.is_ok():
            return self._value
        else:
            return default

    def unwrap_or_else(self, op: t.Callable[[t.Any], t.Any]) -> t.Any:
        if self.is_ok():
            return self._value
        else:
            return op(self._value)

class Ok(_Result):
    def __init__(self, value: t.Any):
        super().__init__(value, True)

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value
        else:
            return False

    def __repr__(self) -> str:
        return f"Ok({self._value})"

class Err(_Result):
    def __init__(self, value: t.Any):
        super().__init__(value, False)

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, Err):
            return self._value == other._value
        else:
            return False

    def __repr__(self) -> str:
        return f"Err({self._value})"