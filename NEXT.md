# whats next

## support for validators with quantifiers (all vs any)

ref: https://en.wikipedia.org/wiki/Quantifier_(linguistics)

### approach A: make it a named scope

```py
# this is very readable
vf.cells.all.positive(col='qty')
vf.cells.any.positive(col='profit_or_loss')

# this is even more human readable
vf.all_cells.positive(col='qty')
vf.any_cells.positive(col='profit_or_loss')

```

### approach B: just make it an arg

not super readable at first glance - a reader wont know until the end of the line about the quantifier. 

```py
vf.cells.positive(col='qty', n=all)
vf.cells.positive(col='profit_or_loss', n=any)
```

but it would be the most straightforward to implement.

its also a cool way to make use of the builtin `any` and `all` functions

in addition it turns out this approach is functional. it takes the quantifier as a kind of function, so others could easily be defined, used, and reused 🏅

```py
vf.cells.positive(col='profit_or_loss', n=atleast(2))
vf.cells.positive(col='profit_or_loss', n=exactly(12))
vf.cells.positive(col='profit_or_loss', n=atmost(100))
```

> quantifier functions would need to be designed to behave like the builtin `any` and `all` functions. 
> ref: https://www.w3schools.com/python/ref_func_any.asp

eg. heres how code for the `atleast` quantifier function would look:

```py
# as a super functional lambda oneliner
atleast = lambda min : lambda iterable : min >= len(filter(lambda is_t : is_t, iterable))

# this other way is much more verbose and pedantic
# but is performant and includes helpful assertions to hint when args are bad
def atleast(min):

  fail_msg = "the quantifier 'atleast {}' makes no sense".format(min)
  assert isinstance(min, int), fail_msg
  assert min > 0, fail_msg

  def atleast_min(iterable):
    truthy_count = 0
    for is_truthy in iterable:
        if is_truthy:
          truthy_count += 1
        if truthy_count >= min:
          return true
    return false

  return atleast_min
```

this flexiblity is not really there with the previous approach - additional boilerplate would be needed for each quantifier to be supported

## pedal to the metal with Ramda helpers

time to double down on the functional approach and use some functional helpers from a package like Ramda

the good:

```py
import ramda as R

vf.cells.validator(R.equals(0))
vf.cells.validator(R.either(R.equals(111),R.equals(-100)))
vf.cells.validator(R.equals(111), filter=R.compose(R.negate, R.is_nil)) # `R.compose` saves the day
```

the bad:

```py
vf.cells.validator(R.flip(R.gte))(0)) # need to flip to actually mean 'cell is greater than 0'
vf.cells.validator(R.equals(111), n=R.all(R.identity)) # same as `n=any` from above but crazy

```

it get even worse when trying to implement `atleast` with Ramda:

ref: https://pypi.org/project/ramda/

```py
# first try
atleast = lambda min : lambda iterable : R.gte(len(R.filter(R.identity, iterable)), min)

# another way
atleast = lambda min : lambda iterable : R.gte(R.count_by(R.identity, iterable), min)
```

that was bad - so lets try again with even more Ramda:

```py
atleast = lambda min : R.compose(R.lte(min), R.count_by(R.identity)) # returns a function that returns `True` if `min` is less than or equal to the number of truthy elements

atleast = lambda min : R.pipe(R.count_by(R.identity), R.lte(min)) # the flipped logic on R.lte is super confusing

atleast = lambda min : R.pipe(R.count_by(R.identity), R.flip(R.gte)(min)) # better or worse than without Ramda?

```

while it might look cool its really not super readable, and the tradeoff is that its not performant and so basically not worth it

## more predefined validators

```py

vf.frame.rows(2)
vf.frame.cols(2)

vf.cells.unique(col='product_id')

vf.cells.sum(0, col=['credit', 'debit']) # for all my accountants
vf.cells.avg(10, col='net_amount')

```

here `unique`, `sum` and `avg` would use a new base validator which validates some reduction of the cell values

eg. heres how code for the `sum` validator would look using the proposed new base validator `vf.cells.reduce_validator`:

```py
validate_sum_of_all_is_zero = vf.cells.reduce_validator( 
  R.equals(0), # validate function
  R.reduce(R.add, 0), # reduce function
  fail_msg = 'sum was not {}'.format(val)
)

# this is the same as above but using the reducer `R.sum` 
validate_sum_of_all_is_zero = vf.cells.reduce_validator(R.equals(0), R.sum, fail_msg = 'sum was not {}'.format(val)) 

# parameterized pass val and selector kwargs
sum = lambda val, **kwargs : vf.cells.reduce_validator(R.equals(val), R.sum, fail_msg = 'sum was not {}'.format(val), **kwargs) 

# this is the same as above but sans lambdas
def sum(val, **kwargs):
  return vf.cells.reduce_validator( 
    R.equals(val),
    R.sum,
    'sum was not {}'.format(val),
    **kwargs
  )

# with builtin instead of all the Ramda
from functools import reduce 
import operator

def sum(val, **kwargs):
  return vf.cells.reduce_validator( 
    lambda x : x == val,
    lambda cells : reduce(operator.add, cells, 0)
    'sum was not {}'.format(val),
    **kwargs
  )  
```

the other base validator `vf.cells.map_validator` which validates the cell values individually may be used a bit more, so it could just take the shorthand alias

```py
vf.cells.map_validator(...) 
vf.cells.validator(...) # alias for `map_validator`
```
