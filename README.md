# validframe
useful validators for pandas dataframes

## Basic usage

```py
import validframe as vf

df = pd.DataFrame(
  columns: ['a','b'], # headers
  data: [
    [1, 1], # row 0
    [1, None] # row 1
    [1, 'hello'] # row 2
    [1, 3.14] # row 3
  ])

vf.cells.validator(lambda x: , col='a')(df)

# validate that all cells that are numbers are also positive
vf.cells.validator(lambda x: x>0, filter=lambda x: isinstance(x, Number) )(df)

vf.cells.positive()(df) # AssertionError
vf.cells.not_empty()(df) # AssertionError
vf.cells.empty()(df) # AssertionError

vf.cells.positive(row=0)(df)
vf.cells.negative(row=0)(df) # AssertionError
vf.cells.not_empty(row=0)(df)
vf.cells.not_empty(row=1)(df) # AssertionError
vf.cells.not_empty(col='a')(df)
vf.cells.not_empty(col='b')(df) # AssertionError

vf.cells.empty(col='b', row=1)(df)
vf.cells.empty(col='b')(df) # AssertionError

vf.cells.min(0, col='a')(df)
vf.cells.max(2, col='a')(df)
vf.cells.minmax(0, 2, col='a')(df)

vf.cells.ints(col='a')(df)
vf.cells.ints(row=0)(df)
vf.cells.ints(col='b')(df) # AssertionError

vf.cells.strs(col='b', row=3)(df)
vf.cells.floats(col='b', row=4)(df)

vf.cells.totals(4, col='a')(df)

```

### boycotting lambdas?

use functions instead
```py
def is_cell_foo(x):
  foo = (None, str, int, float)
  return isinstance(x, foo)

validate_is_cells_foo = vf.cells.validator(is_cell_foo)

validate_is_cells_foo(df)

```