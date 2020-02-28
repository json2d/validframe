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
      vf.FrameValidator(
        lambda df: df.shape[1] == 2, 
        'must have 2 columns'
      ),

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
        cols='a'
      ),

      vf.CellsValidator(
        lambda xs: all([x == 1 for x in xs]), 
        'all must equal 1',
        rows=[0, 3]
      ),

      vf.CellsValidator(
        lambda xs: all([x == -42 or x == 3.14 for x in xs]),
        'all must equal 42 or 3.14',
        cols='b', rows=[0, 3]
      ),

      vf.CellsValidator(
        lambda xs: all([x == 1 for x in xs]), 
        'all must equal 1',
        cols=['a'], rows=[0, 3]
      ),
      
      vf.CellsValidator(
        lambda xs: all([
          x == -42 or x == 3.14 
          for x in filter(lambda x: isinstance(x, int), xs)
        ]),
        'all that are numbers must equal to -42 or 3.14'
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
        cols='b'
      ),

      vf.CellsValidator(
        lambda xs: all([
          x == -42
          for x in filter(lambda x: isinstance(x, int), xs)
        ]),
        'all that are ints must equal to -42',
        cols='b', rows=[0,1,2]
      ),
    ]

    self._test_should_pass(pass_validators, df)

    fail_validators = [
      vf.FrameValidator(
        lambda df: df.shape[0] != 4,
        'must be less than 4 rows'
      ),

      vf.CellsValidator(
        R.all(R.isinstance(Number)),
        'all must be numbers'
      ),

      vf.CellsValidator(
        R.all(R.isinstance(Number)),
        'all in column b must be numbers',
        cols='b'), # all cells in col 'a' are numbers
      
      vf.CellsValidator(
        R.all(R.isinstance(Number)),
        'all in column b must be numbers',
        cols=['b']), # all cells in col 'a' are numbers

      vf.CellsValidator(
        R.all(lambda x: x < 0), 
        'all in row 0 must be less than 0',
        rows=0
      ), # all cells in row 0 and 3 are negative (and numbers)

      vf.CellsValidator(
        R.all(lambda x: x < 0), 
        'all in row 0 and 3 must be less than 0',
        rows=[0, 3]
      ), # all cells in row 0 and 3 are negative (and numbers)

      vf.CellsValidator(
        R.all(lambda x: x < 0), 
        'all in row 0 and 3 and col b must be less than 0',
        cols='b', rows=[0, 3]
      ),

      vf.CellsValidator(
        R.all(lambda x: x < 0), 
        'all in row 0 and 3 and col a must be less than 0', 
        cols=['a'], rows=[0, 3]
      ),

      vf.CellsValidator(
        R.pipe(R.filter(R.isinstance(float)), R.all(lambda x: x < 0)),
        'all floats in in row 1, 3, and 4 and col b must be less than 0', 
        cols=['b'], rows=[4,3,1])
    ]

    self._test_should_fail(fail_validators, df)

unittest.main()