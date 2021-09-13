import collections
import functools
import itertools
import more_itertools
from typing import Callable, Iterable, Mapping, Tuple, TypeVar

from darwin import util


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


def chunk(size: int) -> Callable[[Iterable[A]], Iterable[Tuple]]:
  def __fn(iterable: Iterable[A]) -> Iterable[Tuple]:
    return more_itertools.chunked(iterable, size, strict=False)
  return __fn


def partition(func: Callable[[A], bool]) -> Callable[[Iterable[A]], Tuple[Iterable[A], Iterable[A]]]:
  def __fn(iterable: Iterable[A]) -> Tuple[Iterable[A], Iterable[A]]:
    return more_itertools.partition(func, iterable)
  return __fn


def compact(iterable: Iterable[A]) -> Iterable[A]:
  return filter(bool)(iterable)


def take(size: int) -> Callable[[Iterable[A]], Iterable[A]]:
  def __fn(iterable: Iterable[A]) -> Iterable[A]:
    return more_itertools.take(size, iterable)
  return __fn


def tap(func: Callable[[A], None]) -> Callable[[Iterable[A]], Iterable[A]]:
  def __fn(iterable: Iterable[A]) -> Iterable[A]:
    for element in iterable:
      func(element)
      yield element
  return __fn


def countby(func: Callable[[A], B]) -> Callable[[Iterable[A]], collections.Counter]:
  return util.compose(collections.Counter, map(func))


def flatten(iterable: Iterable[Iterable[A]]) -> Iterable[A]:
  return more_itertools.flatten(iterable)


def flatmap(func: Callable[[A], Iterable[A]]) -> Callable[[Iterable[A]], Iterable[A]]:
  return util.compose(flatten, map(func))


def sortby(func: Callable[[A], B]) -> Callable[[Iterable[A]], Iterable[A]]:
  def __fn(iterable: Iterable[A]) -> Iterable[A]:
    return sorted(iterable, key=func)
  return __fn


def sumby(func: Callable[[A], float]) -> Callable[[Iterable], float]:
  return util.compose(sum, map(func))
