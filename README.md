# validframe
validators for pandas dataframes

## Here we go

```py
import validframe as vf

df = pd.DataFrame([
  ['a','b'], # headers
  [1,2], # row 1
  [1, None] # row 2
  [1, 'hello'] # row 3
  [1, 3.14] # row 4
])

err_msg = "you wont see this error"
err_msg = "you wont see this error"

assert vf.not_negative()(df), "you wont see this error"
assert vf.not_empty()(df), "you will see this error"

assert vf.not_empty(row=0)(df), "you wont see this error"
assert vf.not_empty(row=1)(df), "you will see this error"
assert vf.not_empty(col='a')(df), "you wont see this error"
assert vf.not_empty(col='b')(df), "you will see this error"

assert vf.totals(4, col='a')(df), "you won't see this error"
assert vf.min(0, col='a')(df), "you won't see this error"
assert vf.max(2, col='a')(df), "you won't see this error"

assert vf.ints(col='a')(df), "you won't see this error"
assert vf.ints(col='b')(df), "you will see this error"

assert vf.strs(col='b', row=3)(df), "you won't see this error"
assert vf.floats(col='b', row=4)(df), "you won't see this error"

assert vf.validate(lambda x: x.isnumeric, col='a')(df), "you won't see this error"

# validate that all cells that are numbers are positive
assert vf.validate(lambda x: x>0, filter=lambda x: x.isnumeric() )(df), "you won't see this error"
```

### boycotting lambdas? 
use functions instead
```
def 

