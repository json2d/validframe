import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from datetime import timedelta, datetime

from numbers import Number

# from helpers import *

# from functools import reduce

import unittest
import ramda as R
import pandas as pd

import validframe as vf

class TestEverything(unittest.TestCase):

  # use `_test` prefix isntead of `test` (w/o leading underscore) so test runner doesn't use it
  def _test_should_fail(self, fail_validators, df):
    for validator in fail_validators:
      with self.assertRaises(AssertionError):
        validator.validate(df)

  def _test_should_pass(self, pass_validators, df):
    try:
      for validator in pass_validators:
        validator.validate(df)
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
      vf.frame.validator(
        lambda df: df.shape[0] == 2, 
        'must have 2 columns'
      ),

      vf.cells.validator(
        lambda xs: all([not isinstance(x, Mystery) for x in xs]), 
        'all must not be instances of type Mystery'
      ),

      vf.cells.validator(
        lambda xs: all([x is None or x >= -42 for x in xs]), 
        'all must be None or greater than -42'
      ),

      vf.cells.validator(
        lambda xs: all([x == 1 for x in xs]), 
        'all must equal 1',
        col='a'
      ),

      vf.cells.validator(
        lambda xs: all([x == 1 for x in xs]), 
        'all must equal 1',
        row=[0, 3]
      ),

      vf.cells.validator(
        lambda xs: all([x == -42 or x == 3.14 for x in xs]),
        'all must equal 42 or 3.14',
        col='b', row=[0, 3]
      ),

      vf.cells.validator(
        lambda xs: all([x == 1 for x in xs]), 
        'all must equal 1',
        col=['a'], row=[0, 3]
      ),
      
      vf.cells.validator(
        lambda xs: all([
          x == -42 or x == 3.14 
          for x in filter(lambda x: isinstance(x, int), xs)
        ]),
        'all that are numbers must equal to -42 or 3.14'
      ),

      vf.cells.validator(
        lambda xs: all([
          x is None
          for x in filter(lambda x: not isinstance(x, Number), xs)
        ]),
        'all that are not numbers must be None'
      ),
      
      vf.cells.validator(
        lambda xs: all([
          x == -42
          for x in filter(lambda x: isinstance(x, int), xs)
        ]),
        'all that are ints must equal to -42',
        col='b'
      ),

      vf.cells.validator(
        lambda xs: all([
          x == -42
          for x in filter(lambda x: isinstance(x, int), xs)
        ]),
        'all that are ints must equal to -42',
        col='b', row=[0,1,2]
      ),
    ]

    self._test_should_pass(pass_validators, df)

    fail_validators = [
      vf.frame.validator(
        lambda df: df.shape[1] < 4,
        'must be less than 4 rows'
      ),

      vf.cells.validator(
        R.all(R.is(Number)),
        'all must be numbers'
      ),

      vf.cells.validator(
        R.all(R.is(Number)),
        'all in column b must be numbers',
        , col='b'), # all cells in col 'a' are numbers
      
      vf.cells.validator(
        R.all(R.is(Number)),
        'all in column b must be numbers',
        col=['b']), # all cells in col 'a' are numbers

      vf.cells.validator(
        R.all(lambda x: x < 0), 
        'all in row 0 must be less than 0',
        row=0
      ), # all cells in row 0 and 3 are negative (and numbers)

      vf.cells.validator(
        R.all(lambda x: x < 0), 
        'all in row 0 and 3 must be less than 0',
        row=[0, 3]
      ), # all cells in row 0 and 3 are negative (and numbers)

      vf.cells.validator(
        R.all(lambda x: x < 0), 
        'all in row 0 and 3 and col b must be less than 0',
        col='b', row=[0, 3]
      ),

      vf.cells.validator(
        R.all(lambda x: x < 0), 
        'all in row 0 and 3 and col a must be less than 0', 
        col=['a'], row=[0, 3]
      ),

      vf.cells.validator(
        R.pipe(R.filter(R.is(float)), R.all(lambda x: x < 0)),
        'all floats in in row 1, 3, and 4 and col b must be less than 0', 
        col=['b'], row=[4,3,1])
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
      vf.frame.existant(),
      vf.frame.rows(3),
      vf.frame.cols(4),
      vf.cells.positive(n=any),
      vf.cells.positive(col='a'),
      vf.cells.negative(col='b', row=0),
      vf.cells.empty(n=any),
      vf.cells.empty(col='b', row=[1,2]),
      vf.cells.not_empty(col=['a','c'], row=[0,3]),
      vf.cells.min(0, col=['a','b'], row=3),
      vf.cells.max(3,14, col=['a','b'], row=3),
      vf.cells.minmax(-42, 3.14, filter=R.is(Number)),
      vf.cells.ints(col='a'),
      vf.cells.floats(col='b', row=3),
      vf.cells.strs(col='c'), 
    ]

    self._test_should_pass(pass_validators, df)


    fail_validators = [
      vf.frame.non_existant(),
      vf.frame.rows(1),
      vf.frame.cols(5),
      vf.cells.positive(col='b', row=0),
      vf.cells.negative(col='a'),
      vf.cells.empty(col=['a','c'], row=[0,3]),
      vf.cells.not_empty(col='b', row=[1,2]),
      vf.cells.min(3.14, col=['a','b'], row=3),
      vf.cells.max(0, col=['a','b'], row=3),
      vf.cells.minmax(0, 2, filter=R.is(Number)),
      vf.cells.ints(col='b'),
      vf.cells.floats(col='a'),
      vf.cells.strs(row=3), 
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
      vf.cells.total(4, col='a'), 
      vf.cells.total(-41, col=['a','b'], row=0), 
      vf.cells.total(3.14, col=['a','b'], row=[0,3]), 
      vf.cells.total(-38, filter=lambda x : isinstance(x, int)), 
      vf.cells.total(7.14, filter=lambda x : isinstance(x, Number) and x > 0), 
    ]

    self._test_should_pass(pass_validators, df)


    fail_validators = [
      vf.cells.total(100, col='a'), 
      vf.cells.total(1, row=1), # theres a None in this row
      vf.cells.total('gg', col='c'), 
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
      vf.cells.minmax(some_day, some_day + timedelta(days=1), col='trn_date'),
      vf.cells.min(some_day, col='trn_date'),
      vf.cells.max(some_day + timedelta(days=2), col='trn_date'),
    ]

    self._test_should_pass(pass_validators, df)


    fail_validators = [
      vf.cells.minmax(some_day - timedelta(days=1), some_day, col='trn_date'),
      vf.cells.min(some_day + timedelta(hours=2), col='trn_date'),
      vf.cells.max(some_day + timedelta(hours=2), col='trn_date'),
    ]

    self._test_should_fail(fail_validators, df)


unittest.main()