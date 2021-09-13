import collections
import functools
import itertools
import operator
import unittest

from darwin import iterable


class TestIterable(unittest.TestCase):
  def test_map(self):
    test_fn = functools.partial(operator.add, 5)
    values = range(10)

    self.assertEqual(
      list(iterable.map(test_fn)(values)),
      list(map(test_fn, values))
    )

  def test_filter(self):
    test_fn = functools.partial(operator.lt, 5)
    values = range(10)

    self.assertEqual(
      list(iterable.filter(test_fn)(values)),
      list(filter(test_fn, values)),
    )
  
  def test_reduce(self):
    test_fn = operator.mul
    values = range(10)

    self.assertEqual(
      iterable.reduce(test_fn)(values),
      functools.reduce(test_fn, values)
    )

  def test_fold(self):
    test_fn = operator.mul
    values = range(10)

    self.assertEqual(
      iterable.fold(test_fn)(values)(0),
      functools.reduce(test_fn, values, 0)
    )
  
  def test_scan(self):
    test_fn = operator.mul
    values = range(10)

    self.assertEqual(
      list(iterable.scan(test_fn)(values)(0)),
      list(itertools.accumulate(values, test_fn, initial=0))
    )

  def test_groupby(self):
    Person = collections.namedtuple('Person', ['ID', 'age'])
    test_fn = operator.attrgetter('age')
    values = [
      Person('0', 40),
      Person('1', 40),
      Person('2', 40),
      Person('3', 41),
      Person('4', 41),
      Person('5', 41),
      Person('6', 42),
      Person('7', 43),
      Person('8', 43),
      Person('9', 44)
    ]

    self.assertEqual(
      {k: list(vs) for k, vs in iterable.groupby(test_fn)(values)},
      {k: list(vs) for k, vs in itertools.groupby(values, test_fn)}
    )
