import functools
import inspect
from typing import Callable, Tuple, TypeVar


A = TypeVar
B = TypeVar
C = TypeVar


def curried(func: Callable) -> Callable:
  def __fn(func: Callable, spec: inspect.FullArgSpec):
    def curried_func(*args, **kwargs):
      new_func = functools.partial(func, *args, **kwargs)
      new_spec = inspect.getfullargspec(new_func)
      
      if new_spec.args:
        return __fn(new_func, new_spec)
      else:
        return new_func()
    
    curried_func.func = func
    curried_func.args = spec.args
    curried_func.keywords = spec.kwonlyargs

    return curried_func
  
  return __fn(func, inspect.getfullargspec(func))


def tupled(func: Callable):
    def tupled_func(tupled: Tuple):
        return func(*tupled)
    return tupled_func


def identity(a: A) -> A:
  return a


def constant(b: B) -> Callable[[A], B]:
  def __fn(_: A) -> B:
    return b
  return __fn


def compose(*funcs):
  def __fn(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    def __gn(a: A) -> B:
      return f(g(a))
    return __gn

  return functools.reduce(__fn, funcs)
