from __future__ import annotations
import typing as t

from dataclasses import dataclass

class UnwrapError(Exception):
    pass

class Result:
    pass


T = t.TypeVar('T') # Result type
U = t.TypeVar('U') # Ok function result type
F = t.TypeVar('F') # Err function result type
E = t.TypeVar('E') # Error type
@dataclass
class Ok(Result):
    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def expect(self, msg: str) -> T:
        return self.value

    def expect_err(self, msg: str) -> None:
        raise UnwrapError(msg)

    def unwrap(self) -> T:
        return self.value

    def unwrap_err(self) -> None:
        raise UnwrapError('called `Result::unwrap_err()` on an `Ok` value')

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else(self, f: t.Callable[[], T]) -> T:
        return self.value

    def unwrap_unchecked(self) -> T:
        return self.value

    def And(self, res: Result) -> Result:
        return res

    def AndThen(self, f: t.Callable[[T], Result]) -> Result:
        return f(self.value)

    def Or(self, res: Result) -> Result:
        return self

    def OrElse(self, f: t.Callable[[], Result]) -> Result:
        return self

    def Map(self, f: t.Callable[[T], U]) -> Result[U]:
        return Ok(f(self.value))

    def MapErr(self, f: t.Callable[[E], F]) -> Result[T]:
        return self


T = t.TypeVar('T') # Result type
U = t.TypeVar('U') # Ok function result type
F = t.TypeVar('F') # Err function result type
E = t.TypeVar('E') # Error type
@dataclass
class Err(Result):
    error: t.Any

    def is_err(self) -> bool:
        return True

    def is_ok(self) -> bool:
        return False

    def expect(self, msg: str) -> T:
        raise UnwrapError(msg)

    def expect_err(self, msg: str) -> E:
        return self.error

    def unwrap(self) -> T:
        raise UnwrapError(f"called `Result::unwrap()` on an `Err` value: {self.error}")

    def unwrap_err(self) -> E:
        return self.error

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, f: t.Callable[[], T]) -> T:
        return f(self.error)

    def unwrap_unchecked(self) -> T:
        return self.error

    def And(self, res: Result) -> Result:
        return self

    def AndThen(self, f: t.Callable[[T], Result]) -> Result:
        return self

    def Or(self, res: Result) -> Result:
        return res

    def OrElse(self, f: t.Callable[[], Result]) -> Result:
        return f(self.error)

    def Map(self, f: t.Callable[[T], U]) -> Result[U]:
        return self

    def MapErr(self, f: t.Callable[[E], F]) -> Result[T]:
        return Err(f(self.error))

T = t.TypeVar('T') # Result type
def ok(value: T) -> Result[T]:
    return Ok(value)

E = t.TypeVar('E') # Error type
def err(error: E) -> Result[E]:
    return Err(error)