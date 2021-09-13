import functools
import itertools
from typing import Callable, Iterable, Mapping, TypeVar


A = TypeVar
B = TypeVar


def map(func: Callable[[A], B]) -> Callable[[Iterable[A]], Iterable[B]]:
  def __fn(iterable: Iterable[A]) -> Iterable[B]:
    return (func(item) for item in iterable)
  return __fn


def filter(func: Callable[[A], bool]) -> Callable[[Iterable[A]], Iterable[A]]:
  def __fn(iterable: Iterable[A]) -> Iterable[A]:
    return (item for item in iterable if func(item))
  return __fn


def reduce(func: Callable[[A, A], A]) -> Callable[[Iterable[A]], A]:
  def __fn(iterable: Iterable[A]) -> A:
    return functools.reduce(func, iterable)
  return __fn


def fold(func: Callable[[B, A], B]) -> Callable[[Iterable[A]], Callable[[B], B]]:
  def __fn(iterable: Iterable[A]) -> Callable[[B], B]:
    def __gn(state: B) -> B:
      return functools.reduce(func, iterable, state)
    return __gn
  return __fn


def scan(func: Callable[[B, A], B]) -> Callable[[Iterable[A]], Callable[[B], Iterable[B]]]:
  def __fn(iterable: Iterable[A]) -> Callable[[B], Iterable[B]]:
    def __gn(state: B) -> Iterable[B]:
      return itertools.accumulate(iterable, func, initial=state)
    return __gn
  return __fn


def groupby(func: Callable[[A], B]) -> Callable[[Iterable[A]], Mapping[B, Iterable[A]]]:
  def __fn(iterable: Iterable[A]) -> Mapping[B, Iterable[A]]:
    return itertools.groupby(iterable, key=func)
  return __fn
