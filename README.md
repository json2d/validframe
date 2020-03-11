# 🖼 validframe
[`validium`](https://github.com/json2d/validium) validators for pandas dataframes

## Quick install
```bash
pip install validframe
```

## Basic usage

Need some faith in those frames? Let's dive in.

### Predefined validators

Out-of-the-box you get a set of validators for the considerably more common ways to validate dataframes:

```py
df = pd.DataFrame(
  columns: ['like_counts','comment'], # headers
  data: [
    [42, 'hello world'], # row 0
    [100000, '😆'], # row 1
    [123456, 'lol'], # row 2
    [987, "you're the baz"] # row 3
  ])


validators = [
  vf.frame.not_empty() # frame must be not empty
  vf.frame.empty() # frame must be empty
  vf.frame.rows(4) # frame must have 4 rows
  vf.frame.rows(100) # frame must have 100 rows
  vf.frame.cols(2) # frame must have 2 cols

  vf.cells.all_eq(1, cols=['like_counts']) # all cells must equal 1
  vf.cells.all_is(str, cols=['comment']) # all cells must be instances of str
  vf.cells.all_is(float, cols=['like_counts']) # all cells must be instances of float

  vf.cells.all_gt(0, cols=['like_counts']) # all cells must be greater than 0
  vf.cells.all_lt(0, cols=['like_counts']) # all cells must be less than 0

  vf.cells.sum_eq(-1, cols=['like_counts']) # all cells summed must equal -1
  vf.cells.sum_gt(0, cols=['like_counts']) # all cells summed must be greater than 0
  vf.cells.sum_lt(0, cols=['like_counts']) # all cells summed must be less than 0
  vf.cells.uniq(cols=['like_counts']) # all cells must be unique
]

for v in validators:
  try:
    v.validate(df)
  except AssertionError as err
    print(err)

# AssertionError: frame must be empty
# AssertionError: frame must have 100 rows
# AssertionError: all cells must be instances of float
# AssertionError: all cells must be less than 0
# AssertionError: all cells summed must be less than 0

```

Not exhaustive by any means - just enough to cover the baseline usage.

> Think there are some other common validators that are missing here? Proposals via issues and PRs are welcomed 👍

## More advanced usage

### Custom validators

When none of the predefined validators can do the trick, well its time to roll up your sleeves and create your own validator.

For starters you can create a `CellsValidator` to validate dataframes by their cells:

```py
import validframe as vf

df = pd.DataFrame(
  columns: ['like_counts','comment'], # headers
  data: [
    [42, 'hello world'], # row 0
    [100000, '😆'], # row 1
    [123456, 'lol'], # row 2
    [987, 'earth is definitely flat'] # row 3
  ])

alotta_likes_validator = vf.CellsValidator(
  lambda xs: all([x >= 1000 for x in xs]),
  'all like counts must be atleast 1000'
  cols=['like_counts']
)

alotta_likes_validator.validate(df) # AssertionError: all likes must be atleast 1000

```

You can also create a `RowsValidator` to validate dataframes by their rows:

```py
df = pd.DataFrame(
  columns: ['date', 'total', 'subtotal', 'tax'], # headers\
  data: [
    ['2020-01-11', 108.25, 100, 8.25], 
    ['2010-01-11', 106, 100, 6], 
    ['2009-01-11', 104.50, 100, 4.50] 
  ])

total_validator = vf.RowsValidator(
  lambda rows: all([row['total'] == row['sub_total'] + row['tax'] for row in rows]),
  'all rows must have total equal the sub-total plus tax',
  cols=['total', 'sub_total', 'tax']
)

total_validator.validate(df) # pass
```

If you really enjoy `pandas` then you might prefer to create a `FrameValidator` to validate dataframes utilizing `pandas` and `numpy` to write the logic:

```py

import pandas as pd
import numpy as np

ledger_df = pd.DataFrame(
  columns = ['company', 'balance'],
  data = [
    ['Google', 100000], 
    ['Google', -90000], 
    ['Netflix', -10000], # will be unbalanced
    ['Amazon', 0], 
    ['Google', -10000], 
  ]
)

def is_balanced_by_company(df):
  pivot_df = df.pivot_table(values='balance', columns=['company'], aggfunc=np.sum)
  return pivot_df[pivot_df == 0].count().sum() == 0

balanced_validator = vf.FrameValidator(
  is_balanced_by_company,
  'sum of balances for every company must equals 0'
)

balanced_validator.validate(ledger_df) # AssertionError: sum of balances for every company must equals 0

```

### Go functional

As with [`validium`](https://github.com/json2d/validium) validators in general, using a functional programming library like `ramda` can add brevity and readability to the code for your validation logic.

```py
import ramda as R

# same as above
all_gt_zero_validator = vf.CellsValidator(
  R.all(lambda x: x>0),
  'all cells must be greater than 0'
  cols=['a']
)
```

This is especially true when your validation logic start to become a bit more complex:

```py
sum_numbers_eq_zero_validator = vf.CellsValidator(
  R.compose(R.equals(0), R.sum, R.filter(lambda x: isinstance(x, Number)),
  'all cells that are numbers summed must be greater than 0'
  cols=['credit', 'debit']
)
```

### Max flexibility

Another recommendation would be to use a function instead of a `lambda` when your validation logic can't be expressed comfortably as a onliner, eg. your logic involves making a request to a web API:

```py
import pandas as pd
import request

def match_remote_checksums(df):
  checksums = request.get(REMOTE_CHECKSUM_URL) # just imagine
  remote_df = pd.DataFrame({'checksum': checksums})
  return df.equals(remote_df)

# as a oneliner:
# match_remote_checksums = lambda df: pd.DataFrame({'checksum': request.get(REMOTE_CHECKSUM_URL)}).equals(df)

validator = vf.FrameValidator(
  match_remote_checksums, 
  'checksums must match the set from the server', 
  cols=['checksum']
)
```

