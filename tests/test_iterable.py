import collections
import functools
import itertools
import more_itertools
import operator
import unittest

from more_itertools.recipes import flatten

from darwin import iterable, util


class TestIterable(unittest.TestCase):
  def test_map(self):
    test_fn = functools.partial(operator.add, 5)
    values = range(12)

    self.assertEqual(
      list(iterable.map(test_fn)(values)),
      list(map(test_fn, values))
    )

  def test_filter(self):
    test_fn = functools.partial(operator.lt, 5)
    values = range(12)

    self.assertEqual(
      list(iterable.filter(test_fn)(values)),
      list(filter(test_fn, values)),
    )
  
  def test_reduce(self):
    test_fn = operator.mul
    values = range(12)

    self.assertEqual(
      iterable.reduce(test_fn)(values),
      functools.reduce(test_fn, values)
    )

  def test_fold(self):
    test_fn = operator.mul
    values = range(12)

    self.assertEqual(
      iterable.fold(test_fn)(values)(0),
      functools.reduce(test_fn, values, 0)
    )
  
  def test_scan(self):
    test_fn = operator.mul
    values = range(12)

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
  
  def test_chunk(self):
    values = range(12)

    self.assertEqual(
      list(more_itertools.chunked(values, 2)),
      list(iterable.chunk(2)(values))
    )
  
  def test_partition(self):
    test_fn = lambda x: x % 2 == 0
    values = range(12)

    self.assertEqual(
      list(zip(*more_itertools.partition(test_fn, values))),
      list(zip(*iterable.partition(test_fn)(values)))
    )
  
  def test_compact(self):
    values = [1, None, 0, 4, 5]

    self.assertEqual(
      list(filter(None, values)),
      list(iterable.compact(values))
    )
  
  def test_take(self):
    values = range(12)

    self.assertEqual(
      list(more_itertools.take(5, values)),
      list(iterable.take(5)(values))
    )
  
  def test_countby(self):
    values = range(12)

    self.assertEqual(
      {1: 10, 2: 2},
      iterable.countby(util.compose(len, str))(values)
    )

  def test_flatten(self):
    values = [[1, 2, 3], [4, 5, 6], [7, 8]]

    self.assertEqual(
      list(more_itertools.flatten(values)),
      list(iterable.flatten(values))
    )
  
  def test_flatmap(self):
    test_fn = lambda x: [x]
    values = range(12)

    self.assertEqual(
      list(values),
      list(iterable.flatmap(test_fn)(values))
    )
  
  def test_sortby(self):
    test_fn = lambda x: -1 * x
    values = range(12)

    self.assertEqual(
      list(sorted(values, reverse=True)),
      list(iterable.sortby(test_fn)(values))
    )
  
  def test_sumby(self):
    test_fn = lambda x: -1 * x
    values = range(12)

    self.assertEqual(
      sum(-i for i in values),
      iterable.sumby(test_fn)(values)
    )
