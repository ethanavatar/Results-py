import pytest
import typing as t

from results import Ok, Err, UnwrapError

Result = t.Union[Ok, Err]

@pytest.mark.parametrize("expr", [
    (Ok(1).is_ok()),
    (not Err(1).is_ok()),
])
def test_is_ok(expr: bool):
    assert expr

@pytest.mark.parametrize("expr", [
    (Err(1).is_err()),
    (not Ok(1).is_err()),
])
def test_is_err(expr: bool):
    assert expr

def test_expect_err():
    with pytest.raises(UnwrapError) as excinfo:
        Ok(1).expect_err("msg")

def test_expect():
    msg = "This is an error message"
    assert Ok(1).expect(msg) == 1
    with pytest.raises(UnwrapError) as excinfo:
        Err(1).expect(msg)
    assert excinfo.value.args[0] == msg

def test_unwrap():
    assert Ok(1).unwrap() == 1
    with pytest.raises(UnwrapError) as excinfo:
        Err(1).unwrap()

def test_unwrap_err():
    assert Err(1).unwrap_err() == 1
    with pytest.raises(UnwrapError) as excinfo:
        Ok(1).unwrap_err()

def test_unwrap_unchecked():
    assert Ok(1).unwrap_unchecked() == 1
    assert Err(1).unwrap_unchecked() == 1

@pytest.mark.parametrize("first, second, expected", [
    (Ok(2), Err("late error"), Err("late error")),
    (Err("early error"), Ok("foo"), Err("early error")),
    (Err("not a 2"), Err("late error"), Err("not a 2")),
    (Ok(2), Ok("different result type"), Ok("different result type")),
])
def test_and(first: Result, second: Result, expected: Result):
    assert first.And(second) == expected

@pytest.mark.parametrize("first, expected", [
    (Ok(2), Ok("4")),
    (Ok(1_000_000), Err("overflowed")),
    (Err("not a number"), Err("not a number")),
])
def test_and_then(first: Result, expected: Result):
    import ctypes

    checked_multiply: t.Callable[[ctypes.c_uint32, ctypes.c_uint32], Result[ctypes.c_uint32]] = lambda x, y: Ok(x * y) if x * y < 4294967295 else Err(x * y)
    sq_then_to_str: t.Callable[[ctypes.c_uint32], str] = lambda x: Ok(str(checked_multiply(x, x).unwrap())) if checked_multiply(x, x).is_ok() else Err("overflowed")

    assert first.And_then(sq_then_to_str) == expected

@pytest.mark.parametrize("first, second, expected", [
    (Ok(2), Err("late error"), Ok(2)),
    (Err("early error"), Ok(2), Ok(2)),
    (Err("not a 2"), Err("late error"), Err("late error")),
    (Ok(2), Ok(100), Ok(2)),
])
def test_or(first: Result, second: Result, expected: Result):
    assert first.Or(second) == expected

sq = lambda x: Ok(x * x)
err = lambda x: Err(x)

@pytest.mark.parametrize("first, fn1, fn2, expected", [
    (Ok(2), sq, sq, Ok(2)),
    (Ok(2), err, sq, Ok(2)),
    (Err(3), sq, err, Ok(9)),
    (Err(3), err, err, Err(3)),
])
def test_or_else(first: Result, fn1: Result, fn2: Result, expected: Result):
    assert first.Or_else(fn1).Or_else(fn2) == expected

@pytest.mark.parametrize("first, expected", [
    (Ok(9).unwrap_or(2), 9),
    (Err(3).unwrap_or(2), 2),
])
def test_unwrap_or(first: Result, expected: int):
    assert first == expected

@pytest.mark.parametrize("first, expected", [
    (Ok(2).unwrap_or_else(len), 2),
    (Err("foo").unwrap_or_else(len), 3),
])
def test_unwrap_or_else(first: Result, expected: int):
    assert first == expected