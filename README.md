# validframe
validators for pandas dataframes

## Here we go

```py
import validframe as vf

df = pd.DataFrame([
  ['a','b'], # headers
  [1, 1], # row 10
  [1, None] # row 1
  [1, 'hello'] # row 2
  [1, 3.14] # row 3
])

vf.validator(lambda x: , col='a')(df)

# validate that all cells that are numbers are also positive
vf.validator(lambda x: x>0, filter=lambda x: isinstance(x, Number) )(df)


vf.positive()(df) # AssertionError
vf.not_empty()(df) # AssertionError
vf.empty()(df) # AssertionError

vf.not_empty(row=0)(df)
vf.not_empty(row=1)(df) # AssertionError
vf.not_empty(col='a')(df)
vf.not_empty(col='b')(df) # AssertionError

vf.empty(col='b', row=1)(df)
vf.empty(col='b')(df) # AssertionError

vf.min(0, col='a')(df)
vf.max(2, col='a')(df)

vf.ints(col='a')(df)
vf.ints(row=0)(df)
vf.ints(col='b')(df) # AssertionError

vf.strs(col='b', row=3)(df)
vf.floats(col='b', row=4)(df)

vf.totals(4, col='a')(df)

```

### boycotting lambdas? 
use functions instead
```py
def is_cell_foo(x):
  foo = (None, str, int, float)
  return isinstance(x, foo)

validate_is_cells_foo = vf.validator(is_cell_foo)

validate_is_cells_foo(df)

```