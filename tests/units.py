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
import numpy as np

import validframe as vf

class TestEverything(unittest.TestCase):

  # use `_test` prefix isntead of `test` (w/o leading underscore) so test runner doesn't use it
  def _test_should_fail(self, fail_validators, df):
    for validator in fail_validators:
      with self.assertRaises(AssertionError):
        validator.validate(df)
        print('fail expected:', validator._v.msg)

  def _test_should_pass(self, pass_validators, df):
    try:
      for validator in pass_validators:
        validator.validate(df)
    except:
      print('pass expected:', validator._v.msg)
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

      vf.RowsValidator(
        lambda rows: all([row['a'] == 1 for row in rows]), 
        'all rows must have \'a\' equal 1'
      ),

      vf.RowsValidator(
        lambda rows: all([row['a'] == 1 for row in rows]), 
        'all rows must have \'b\' equal 1',
        rows=[1,2]
      ),

      vf.RowsValidator(
        lambda rows: all([row['a'] == 1 for row in rows]), 
        'all rows must have \'b\' equal 1',
        cols=['a']
      ),

      vf.RowsValidator(
        lambda rows: all([row['a'] == 1 for row in rows]), 
        'all rows must have \'b\' equal 1',
        cols=['a'], rows=[1,2]
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

    for v in pass_validators : self.assertTrue(v.confirm(test_df))

    self._test_should_pass(pass_validators, test_df)

    fail_validators = [

      vf.CellsValidator(
        R.all(R.is_(Number)),
        'all must be numbers'
      ),

      vf.CellsValidator(
        R.all(R.is_(Number)),
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
        R.pipe(R.filter(R.is_(float)), R.all(lambda x: x < 0)),
        'all floats in in row 0, 2, and 3 and col b must be less than 0', 
        cols=['b'], rows=[3,2,0]
      ),

      vf.RowsValidator(
        lambda rows: all([row['a'] == 3.14 for row in rows]), 
        'all rows must have \'a\' equal 3.14'
      ),

      vf.RowsValidator(
        lambda rows: all([row['a'] == 3.14 for row in rows]), 
        'all rows must have \'a\' equal 3.14',
        rows=[1,2]
      ),

    ]

    self._test_should_fail(fail_validators, test_df)


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
      vf.CellsValidator(
        lambda xs: all([not isinstance(x, Mystery) for x in xs]), 
        'all must not be instances of type Mystery'
      ),

      vf.RowsValidator(
        lambda rows: all([row['a'] == 1 for row in rows]), 
        'all rows must have \'a\' equal 1'
      ),

      vf.FrameValidator(
        lambda df: df.loc[[0,3],['a']][df == 1].count().sum() == len(df.loc[[0,3],['a']]), 
        'all must equal 1'
      ),
    ]

    self._test_should_pass(pass_validators, test_df)

    for v in pass_validators : self.assertTrue(v.confirm(test_df))

    fail_validators = [

      vf.CellsValidator(
        R.all(R.is_(Number)),
        'all must be numbers'
      ),

      vf.RowsValidator(
        lambda rows: all([row['a'] == 3.14 for row in rows]), 
        'all rows must have \'a\' equal 3.14'
      ),

      vf.FrameValidator(
        lambda df: df.loc[[0,3],['a']][df != 1].count().sum() == len(df.loc[[0,3],['a']]), 
        'all must not equal 1'
      ),
    ]

    self._test_should_fail(fail_validators, test_df)

    for v in fail_validators : self.assertFalse(v.confirm(test_df))


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

  def test_more_predefined(self):
    test_df = pd.DataFrame(
      columns = ['like_counts','comment'], # headers
      data = [
        [42, 'hello world'], # row 0
        [100000, '😆'], # row 1
        [123456, 'lol'], # row 2
        [987, "you're the baz"] # row 3
      ])

    pass_validators = [

      vf.cells.all_is(str, cols=['comment']), # all cells must be instances of <str>
      vf.cells.all_gt(0, cols=['like_counts']), # all cells must be greater than 0
      vf.cells.all_gte(0, cols=['like_counts']), # all cells must be greater than or equal to 0

      vf.cells.some_eq(42, cols=['like_counts']), # some cells must equal 42
      vf.cells.some_gte(123456, cols=['like_counts']), # some cells must be greater than or equal to 100000
      vf.cells.some_lte(42, cols=['like_counts']), # some cells must be less than or equal to 987

      vf.cells.none_eq(0, cols=['like_counts']), # no cells must equal 0
      vf.cells.none_is(str, cols=['like_counts']), # no cells must be instances of <str>
      vf.cells.none_lt(42, cols=['like_counts']), # no cells must be less than 42
      vf.cells.none_gt(123456, cols=['like_counts']), # no cells must be greater than or equal to 100000

      vf.cells.some_or_none_eq(0, cols=['like_counts']), # some or no cells must equal 0
      vf.cells.some_or_none_lt(0, cols=['like_counts']), # some or no cells must be less than 0
      vf.cells.some_or_none_lte(0, cols=['like_counts']), # some or no cells must be less than or equal to 0

      vf.cells.all_or_none_is(str, cols=['comment']), # all or no cells must be instances of <str>
      vf.cells.all_or_none_gt(123456, cols=['like_counts']), # all or no cells must be greater than 100000
      vf.cells.all_or_none_lt(42, cols=['like_counts']), # all or no cells must be less than 987

      vf.cells.all_or_some_is(str, cols=['comment']), # all or some cells must be instances of <str>
      vf.cells.all_or_some_gte(123456, cols=['like_counts']), # all or some cells must be greater than or equal to 100000
      vf.cells.all_or_some_lte(42, cols=['like_counts']), # all or some cells must be less than or equal to 42   

      vf.cells.sum_gt(0, cols=['like_counts']), # all cells summed must be greater than 0
      vf.cells.sum_gte(0, cols=['like_counts']), # all cells must be greater than or equal to 0
    ]
    
    self._test_should_pass(pass_validators, test_df)

    fail_validators = [

      vf.cells.all_eq(1, cols=['like_counts']), # all cells must equal 1
      vf.cells.all_lt(0, cols=['like_counts']), # all cells must be less than to 0
      vf.cells.all_lte(0, cols=['like_counts']), # all cells must be less than or equal to 0

      vf.cells.some_is(type(np.nan), cols=['comment']), # some cells must be instances of <numpy.nan>
      vf.cells.some_gt(123456, cols=['like_counts']), # some cells must be greater than 100000
      vf.cells.some_lt(42, cols=['like_counts']), # some cells must be less than 987

      vf.cells.none_gte(123456, cols=['like_counts']), # no cells must be greater than 100000
      vf.cells.none_lte(42, cols=['like_counts']), # no cells must be less than or equal to 42   

      vf.cells.some_or_none_is(str, cols=['comment']), # some or no cells must be instances of <str>
      vf.cells.some_or_none_gt(0, cols=['like_counts']), # some or no cells must be greater than 0
      vf.cells.some_or_none_gte(0, cols=['like_counts']), # some or no cells must be greater than or equal to 0

      vf.cells.all_or_none_eq(42, cols=['like_counts']), # all or no cells must equal 42
      vf.cells.all_or_none_gte(123456, cols=['like_counts']), # all or no cells must be greater than or equal to 100000
      vf.cells.all_or_none_lte(42, cols=['like_counts']), # all or no cells must be less than or equal to 987

      vf.cells.all_or_some_eq(0, cols=['like_counts']), # all or some cells must equal 0
      vf.cells.all_or_some_gt(123456, cols=['like_counts']), # all or some cells must be greater than 100000
      vf.cells.all_or_some_lt(42, cols=['like_counts']), # all or some cells must be less than 42

      vf.cells.sum_eq(-1, cols=['like_counts']), # all cells summed must equal -1
      vf.cells.sum_lt(0, cols=['like_counts']), # all cells summed must be less than 0
      vf.cells.sum_lte(0, cols=['like_counts']), # all cells must be less than or equal to 0

    ]

    self._test_should_fail(fail_validators, test_df)


  def test_uniq(self):
    test_df = pd.DataFrame(
      columns = ['like_counts','comment', 'post_id'], # headers
      data = [
        [42, 'hello world', 111], # row 0
        [100000, '😆', 111], # row 1
        [123456, 'lol', 111], # row 2
        [987, "you're the baz", 101] # row 3
      ])

    pass_validators = [
      vf.rows.uniq(),
      vf.rows.uniq(cols=['comment']),
      vf.rows.uniq(cols=['comment', 'post_id']),
    ]
    
    self._test_should_pass(pass_validators, test_df)

    fail_validators = [
      vf.rows.uniq(cols=['post_id']),
    ]

    self._test_should_fail(fail_validators, test_df)    

unittest.main()