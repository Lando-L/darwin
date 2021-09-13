import functools
import operator
import unittest


from darwin import util


class TestUtil(unittest.TestCase):
  def test_curried(self):
    test_fn = operator.add
    curried_fn = util.curried(operator.add)

    self.assertEqual(
      test_fn(2, 40),
      curried_fn(2)(40),
      'Should be 42'
    )
  
  def test_tupled(self):
    test_fn = operator.add
    tupled_fn = util.tupled(operator.add)

    self.assertEqual(
      test_fn(2, 40),
      tupled_fn((2, 40)),
      'Should be 42'
    )
  
  def test_identity(self):
    self.assertEqual(
      util.identity(42),
      42,
      'Should be 42'
    )
  
  def test_constant(self):
    test_fn = util.constant(42)

    self.assertEqual(
      test_fn('Something Else'),
      42,
      'Should be 42'
    )
  
  def test_compose(self):
    test_fn = util.compose(
      functools.partial(operator.add, 2),
      functools.partial(operator.mul, 10)
    )

    self.assertEqual(
      test_fn(4),
      42,
      'Should be 42'
    )
