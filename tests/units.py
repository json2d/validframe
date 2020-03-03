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

# extensions for some missing ramda functions
R.isinstance = lambda x: lambda y: isinstance(y,x)

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

    test_df = pd.DataFrame(
      columns = ['a','b'],
      data = [
        [1, -42], # row 0
        [1, None], # row 1
        [1, None], # row 2
        [1, 3.14], # row 3
      ],
      dtype=object # prevent None from being converted to np.nan - ref: https://stackoverflow.com/a/48453225
    )
    
    class Mystery():
      pass

    pass_validators = [
      vf.FrameValidator(
        lambda df: 'a' in df.columns, 
        'must have the column "a"'
      ),

      vf.frame.not_empty(),
      vf.frame.rows(4),
      vf.frame.cols(2),

      vf.CellsValidator(
        lambda xs: all([not isinstance(x, Mystery) for x in xs]), 
        'all must not be instances of type Mystery'
      ),

      vf.CellsValidator(
        lambda xs: all([x is None or x >= -42 for x in xs]), 
        'all must be None or greater than -42'
      ),

      vf.CellsValidator(
        lambda xs: all([x == 1 for x in xs]), 
        'all must equal 1',
        cols=['a']
      ),

      vf.CellsValidator(
        lambda xs: all([x == 1 for x in xs]), 
        'all must equal 1',
        cols=['a'], rows=[0, 3]
      ),

      vf.FrameValidator(
        lambda df: df.loc[[0,3],['a']][df == 1].count().sum() == len(df.loc[[0,3],['a']]), 
        'all must equal 1'
      ),

      vf.CellsValidator(
        lambda xs: all([x == -42 or x == 3.14 for x in xs]),
        'all must equal 42 or 3.14',
        cols=['b'], rows=[0, 3]
      ),

      vf.CellsValidator(
        lambda xs: all([x == 1 for x in xs]), 
        'all must equal 1',
        cols=['a'], rows=[0, 3]
      ),
      
      vf.CellsValidator(
        lambda xs: all([
          x == -42 or x == 1
          for x in filter(lambda x: isinstance(x, int), xs)
        ]),
        'all that are int must equal to -42 or 1'
      ),

      vf.CellsValidator(
        lambda xs: all([
          x is None
          for x in filter(lambda x: not isinstance(x, Number), xs)
        ]),
        'all that are not numbers must be None'
      ),
      
      vf.CellsValidator(
        lambda xs: all([
          x == -42
          for x in filter(lambda x: isinstance(x, int), xs)
        ]),
        'all that are ints must equal to -42',
        cols=['b']
      ),

      vf.CellsValidator(
        lambda xs: all([
          x == -42
          for x in filter(lambda x: isinstance(x, int), xs)
        ]),
        'all that are ints must equal to -42',
        cols=['b'], rows=[0,1,2]
      ),
    ]

    self._test_should_pass(pass_validators, test_df)

    fail_validators = [

      vf.frame.empty(),
      vf.frame.rows(10),
      vf.frame.cols(1),

      vf.CellsValidator(
        R.all(R.isinstance(Number)),
        'all must be numbers'
      ),

      vf.CellsValidator(
        R.all(R.isinstance(Number)),
        'all in column b must be numbers',
        cols=['b']), # all cells in col 'a' are numbers

      vf.CellsValidator(
        R.all(lambda x: x < 0), 
        'all in row 0 must be less than 0',
        rows=[0]
      ), # all cells in row 0 and 3 are negative (and numbers)

      vf.CellsValidator(
        R.all(lambda x: x < 0), 
        'all in row 0 and 3 must be less than 0',
        rows=[0, 3]
      ), # all cells in row 0 and 3 are negative (and numbers)

      vf.CellsValidator(
        R.all(lambda x: x < 0), 
        'all in row 0 and 3 and col b must be less than 0',
        cols=['b'], rows=[0, 3]
      ),

      vf.CellsValidator(
        R.all(lambda x: x < 0), 
        'all in row 0 and 3 and col a must be less than 0', 
        cols=['a'], rows=[0, 3]
      ),

      vf.CellsValidator(
        R.pipe(R.filter(R.isinstance(float)), R.all(lambda x: x < 0)),
        'all floats in in row 0, 2, and 3 and col b must be less than 0', 
        cols=['b'], rows=[3,2,0])
    ]

    self._test_should_fail(fail_validators, test_df)


  def test_predefined(self):

    test_df = pd.DataFrame(
      columns = ['a','b'],
      data = [
        [1, -42], # row 0
        [1, None], # row 1
        [1, None], # row 2
        [1, 3.14], # row 3
      ],
      dtype=object # prevent None from being converted to np.nan - ref: https://stackoverflow.com/a/48453225
    )
    
    pass_validators = [
      vf.frame.not_empty(),
      vf.frame.rows(4),
      vf.frame.cols(2),

      vf.cells.all_is(int, cols=['a']),
      vf.cells.all_is(type(None), cols=['b'], rows=[1,2]),
      
      vf.cells.all_eq(1, cols=['a']),
      vf.cells.all_gt(0, rows=[3]),
      vf.cells.all_lt(0, cols=['b'], rows=[0]),

      vf.cells.sum_eq(4, cols=['a']),
      vf.cells.sum_gt(4, rows=[3]),
      vf.cells.sum_lt(4, rows=[0]),
    ]

    self._test_should_pass(pass_validators, test_df)

    fail_validators = [

      vf.frame.empty(),
      vf.frame.rows(10),
      vf.frame.cols(1),

      vf.cells.all_is(int),
      vf.cells.all_is(type(None)),

      vf.cells.all_eq(100, cols=['a']),
      vf.cells.all_gt(100, rows=[3]),
      vf.cells.all_lt(-100, cols=['b'], rows=[0]),

      vf.cells.sum_eq(0, cols=['a']),
      vf.cells.sum_gt(100, rows=[3]),
      vf.cells.sum_lt(-100, rows=[0]),
    ]

    self._test_should_fail(fail_validators, test_df)

unittest.main()