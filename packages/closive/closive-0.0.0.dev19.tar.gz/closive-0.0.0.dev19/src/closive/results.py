"""Results Monad"""
from typing import Generic, TypeVar, Callable, Union

T, E = TypeVar("T"), TypeVar("E")

class Result(Generic[T, E]):
    """A simple Result monad: Ok wraps a success, Err wraps a failure."""
    __slots__ = ("ok", "value")

    def __init__(self, ok: bool, value: Union[T, E]):
        self.ok = ok
        self.value = value

    @staticmethod
    def Ok(val: T) -> "Result[T, E]":
        return Result(True, val)

    @staticmethod
    def Err(err: E) -> "Result[T, E]":
        return Result(False, err)

    def map(self, fn: Callable[[T], T]) -> "Result[T, E]":
        if not self.ok:
            return self  # propagate the Err unchanged
        try:
            return Result.Ok(fn(self.value))
        except Exception as e:
            return Result.Err(e)

    def bind(self, fn: Callable[[T], "Result[T, E]"]) -> "Result[T, E]":
        if not self.ok:
            return self
        try:
            return fn(self.value)
        except Exception as e:
            return Result.Err(e)

    def unwrap(self) -> T:
        if self.ok:
            return self.value
        else:
            raise RuntimeError(f"Called unwrap on Err({self.value!r})")

    def map_error(self, fn: Callable[[E], E]) -> "Result[T, E]":
        if self.ok:
            return self
        try:
            return Result.Err(fn(self.value))
        except Exception as e:
            return Result.Err(e)

    def recover(self, fn: Callable[[E], T]) -> "Result[T, E]":
        if self.ok:
            return self
        try:
            return Result.Ok(fn(self.value))
        except Exception as e:
            return Result.Err(e)

    def unwrap_or(self, default: T) -> T:
        return self.value if self.ok else default

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        return self.value if self.ok else fn(self.value)
