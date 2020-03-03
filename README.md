# validframe
useful validators for pandas dataframes

## Basic usage

Here's how to create a basic validator for list of cells using `CellsValidator`:

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

all_gt_zero_validator = vf.CellsValidator(
  lambda xs: all([x>0 for x in xs]),
  'all cells must be greater than 0'
  cols=['a']
)

all_gt_zero_validator.validate(df) # AssertionError: all cells must be greater than 0

```

### Going functional?

Using a functional programming library like `ramda` can make your validation logic code alot cleaner and readable

```py
# same as above
all_gt_zero_validator = vf.CellsValidator(
  R.all(lambda x: x>0),
  'all cells must be greater than 0'
  cols=['a']
)
```

This is especially true when the validation logic start to become a bit more complex:

```py
sum_numbers_eq_zero_validator = vf.CellsValidator(
  R.compose(R.equals(0), R.sum, R.filter(lambda x: isinstance(x, Number)),
  'all cells that are numbers summed must be greater than 0'
  cols=['credit', 'debit']
)
```

### Boycotting lambdas?

Using functions instead works just fine

```py
def all_gt_zero(xs):
  return all([x>0 for x in xs])

all_gt_zero_validator = vf.CellsValidator(all_gt_zero, 'all cells must be greater than 0')
```

### Predefined validators

Here are a couple of super common validators for the sake of convenience:

```py
vf.cells.all_eq(1, cols=['a']).validate(df) 
vf.cells.all_is(type(None)).validate(df) # AssertionError

vf.cells.all_gt(0, rows=[0]).validate(df)
vf.cells.all_lt(0, rows=[0]).validate(df) # AssertionError

vf.cells.sum_eq(4, cols=['a']).validate(df)
vf.cells.sum_gt(0, cols=['a']).validate(df)
vf.cells.sum_lt(10, cols=['a']).validate(df)
```

Think there are some other validators that should be included? Issues and PRs welcomed!