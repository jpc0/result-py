from __future__ import annotations
from typing import Callable, Any, Generic, TypeVar
from functools import partial

T = TypeVar("T")
U = TypeVar("U")


class Ok(Generic[T]):
    __match_args__ = ("value",)
    __slots__ = ("value")

    value: T

    def __init__(self, value: T):
        if isinstance(value, Ok):
            self.value = value.value
        elif isinstance(value, Err):
            raise Exception("Cannot convert Err to Ok") # TODO: Implement custom exception here
        else:
            self.value = value

    def bind(
        self, func: Callable[[Any], Result[T, U]]
    ) -> Result[T, U]:
        return func(self.value)

    def map(self, func: Callable[[T], Any]) -> Ok[T]:
        return Ok(func(self.value))

    def apply(
        self, func: Ok[Callable[[T], U]]
    ) -> Ok[U]:
        return Ok(func.value(self.value))

    def __iter__(self):
        return ResultIterable(self.value)


class Err(Generic[U]):
    __match_args__ = ("value",)
    __slots__ = ("value")

    value: U

    def __init__(self, value: U):
        if isinstance(value, Ok | Err):
            self.value = value.value
        else:
            self.value = value

    def bind(self, _: Callable[[Any], Result]) -> Err[U]:
        return self

    def map(self, _: Callable[[Any], Any]) -> Err[U]:
        return self

    def apply(
        self, _: Result[Callable[[U], Any]]
    ) -> Err[U]:
        return self

    def __iter__(self):
        return ResultIterable(self.value)

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"


class ResultIterable:
    def __init__(self, value):
        self.returned = False
        self.value = value

    def __next__(self):
        if not self.returned:
            self.returned = True
            return self.value
        raise StopIteration()


Result = Ok[T] | Err[U]
