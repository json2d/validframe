import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from datetime import timedelta, datetime

from numbers import Number

# from helpers import *

# from functools import reduce

import unittest

import pandas as pd

import validframe as vf

class TestEverything(unittest.TestCase):

  # use `_test` prefix isntead of `test` (w/o leading underscore) so test runner doesn't use it
  def _test_should_fail(self, fail_validators, df):
    for validate in fail_validators:
      with self.assertRaises(AssertionError):
        validate(df)

  def _test_should_pass(self, pass_validators, df):
    try:
      for validate in pass_validators:
        validate(df)
    except:
      self.fail('validation should have passed but exception was raised')

  def test_base(self):

    df = pd.DataFrame(
      columns = ['a','b'],
      data = [
        [1, -42], # row 1
        [1, None], # row 2
        [1, None], # row 3
        [1, 3.14], # row 4
      ])
    
    class Mystery():
      pass

    pass_validators = [
      vf.validator(lambda x: not isinstance(x, Mystery)),
      vf.validator(lambda x: x is None or x >= -42),
      vf.validator(lambda x: x == 1, col='a'),
      vf.validator(lambda x: x == 1, row=[0, 3]),

      vf.validator(lambda x: x == -42 or x == 3.14, col='b', row=[0, 3]),
      vf.validator(lambda x: x == 1, col=['a'], row=[0, 3]),
      
      vf.validator(lambda x: x == 1 or x == -42, filter=lambda x: isinstance(x, int)),
      vf.validator(lambda x: x is None, filter=lambda x: not isinstance(x, Number)),
      
      vf.validator(lambda x: x == -42, col='b', filter=lambda x: isinstance(x, int)),
      vf.validator(lambda x: x == -42, col='b', row=[0,1,2], filter=lambda x: isinstance(x, int))
    ]

    self._test_should_pass(pass_validators, df)

    fail_validators = [
      vf.validator(lambda x: isinstance(x, Number)), # all cells are numbers
      vf.validator(lambda x: isinstance(x, Number), col='b'), # all cells in col 'a' are numbers
      vf.validator(lambda x: isinstance(x, Number), col=['b']), # all cells in col 'a' are numbers

      vf.validator(lambda x: x < 0, row=0), # all cells in row 0 and 3 are negative (and numbers)
      vf.validator(lambda x: x < 0, row=[0, 3]), # all cells in row 0 and 3 are negative (and numbers)
      vf.validator(lambda x: x < 0, col='b', row=[0, 3]),
      vf.validator(lambda x: x < 0, col=['a'], row=[0, 3]),

      vf.validator(lambda x: x < 0, filter=lambda x: isinstance(x, Number)),
      vf.validator(lambda x: x < 0, col=['b'], row=[4,3,1], filter=lambda x: isinstance(x, float))
    ]

    self._test_should_fail(fail_validators, df)


  def test_mappers(self):

    df = pd.DataFrame(
      columns = ['a', 'b', 'c'], # headers
      data = [
        ['a', 'b', 'c'], # headers
        [1, -42, 'hello'], # row 0
        [1, None, 'world'], # row 1
        [1, None, 'ciao'], # row 2
        [1, 3.14, 'mondo'], # row 3
      ])

    pass_validators = [
      vf.positive(col='a'),
      vf.negative(col='b', row=0),
      vf.empty(col='b', row=[1,2]),
      vf.not_empty(col=['a','c'], row=[0,3]),
      vf.min(0, col=['a','b'], row=3),
      vf.max(3,14, col=['a','b'], row=3),
      vf.minmax(-42, 3.14, filter=lambda x : isinstance(x, Number)),
      vf.ints(col='a'),
      vf.floats(col='b', row=3),
      vf.strs(col='c'), 
    ]

    self._test_should_pass(pass_validators, df)


    fail_validators = [
      vf.positive(col='b', row=0),
      vf.negative(col='a'),
      vf.empty(col=['a','c'], row=[0,3]),
      vf.not_empty(col='b', row=[1,2]),
      vf.min(3.14, col=['a','b'], row=3),
      vf.max(0, col=['a','b'], row=3),
      vf.minmax(0, 2, filter=lambda x : isinstance(x, Number)),
      vf.ints(col='b'),
      vf.floats(col='a'),
      vf.strs(row=3), 
    ]


    self._test_should_fail(fail_validators, df)

  def test_reducers(self):

    df = pd.DataFrame(
      columns = ['a', 'b', 'c'], # headers
      data = [
        [1, -42, 'hello'], # row 0
        [1, None, 'world'], # row 1
        [1, None, 'ciao'], # row 2
        [1, 3.14, 'mondo'] # row 3
      ])


    pass_validators = [
      vf.totals(4, col='a'), 
      vf.totals(-41, col=['a','b'], row=0), 
      vf.totals(3.14, col=['a','b'], row=[0,3]), 
      vf.totals(-38, filter=lambda x : isinstance(x, int)), 
      vf.totals(7.14, filter=lambda x : isinstance(x, Number) and x > 0), 
    ]

    self._test_should_pass(pass_validators, df)


    fail_validators = [
      vf.totals(100, col='a'), 
      vf.totals(1, row=1), # theres a None in this row
      vf.totals('gg', col='c'), 
    ]

    self._test_should_fail(fail_validators, df)


  def test_with_datetime(self):

    some_day = datetime(2020, 1, 6)

    df = pd.DataFrame(
      columns = ['net_amount', 'product_name', 'trn_date'], # headers
      data = [        
        [5.50, 'canoli', some_day], # row 0
        [9.50, 'tiramisu', some_day + timedelta(hours=1)], # row 1
        [10, 'salad', some_day + timedelta(hours=2)], # row 2
        [10, 'bread', some_day + timedelta(days=1)], # row 3
      ])

    pass_validators = [
      vf.minmax(some_day, some_day + timedelta(days=1), col='trn_date'),
      vf.min(some_day, col='trn_date'),
      vf.max(some_day + timedelta(days=2), col='trn_date'),
    ]

    self._test_should_pass(pass_validators, df)


    fail_validators = [
      vf.minmax(some_day - timedelta(days=1), some_day, col='trn_date'),
      vf.min(some_day + timedelta(hours=2), col='trn_date'),
      vf.max(some_day + timedelta(hours=2), col='trn_date'),
    ]

    self._test_should_fail(fail_validators, df)


unittest.main()