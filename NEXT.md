# whats next

> ### Disclaimer 
> The contents of this file is a fairly coherent stream of conscience brainstorm about different direction to take the design of this library, and intended to be documentation with accurate code examples that reflect how you would actually use the library. For that refer to `README.md`

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


## how about combining the base validators into one to make it even simpler

so what if we just made `cells` the parameter for a base validator function. we already do this with the `vf.frame.validator`:

```py
vf.frame.validator(lambda frame : frame.shape[0] == 2) # validate that frame has 2 columns
```

so this:
```py
# validate that there are any cells whose value is a numbers
vf.cells.validator(any, lambda cell : isinstance(cell, Number), col='a') 
```

we would be rewritten like this:

```py
# validate that there are any cells whose value is a numbers
vf.cells.validator(lambda cells : any([isinstance(cell, Number) for cell in cells]), col='a') 
```

the quantifier (`any`) is no longer parameterized - its the dev's discrestion how to they want to implement/integrate quantifiers in their validation

this 'takes off the training wheels' is arguably a negative tradeoff, but the [flexibily] that emerges is arguably a very postive tradeoff and especially for functional programmers who enjoy Ramda code golf:

```py
# all three just do the same thing
vf.cells.validator(lambda cells : any([isinstance(cell, Number) for cell in cells]), col='a') 
vf.cells.validator(R.all(lambda cell : isinstance(cell, Number))), col='a') 
vf.cells.validator(R.all(R.is(Number))), col='a') 
```

so by making a validator that does less, we're able to do more as the dev 

another thing plus is that we can describe reduction validators, and do it pretty tersely

```py
vf.cells.validator(lambda cells : reduce(operator.add, cells, 0) == 0) # validate that the sum of all cells is 0
```

more Ramda code golf:

```py
# all three just do the same thing
vf.cells.validator(lambda cells : reduce(operator.add, cells, 0) == 0)
vf.cells.validator(lambda cells : R.sum(cells) == 0)
vf.cells.validator(R.compose(R.equals(0), R.sum))
vf.cells.validator(R.pipe(R.sum, R.equals(0)))
```

so should we hitch our wagon with Ramda? lets explore some ore

```py
# validate that 0 is less than all cells that are numbers
vf.cells.validator(R.all(R.lt(0)), filter=R.is(Number))(df)

# validate that sum of cells that are 0 equals 0
vf.cells.validator(R.compose(R.equals(0), R.sum), filter=R.is(Number))(df)

# validate that mean of cells that 0 is less than equals 3.14
vf.cells.validator(R.compose(R.equals(3.14), R.mean), filter=R.lt(0))

# validate that any cells that 0 is less than equals 3.14
vf.cells.validator(R.any(R.equals(3.14)), filter=R.lt(0))

```

```py
vf.cells.validator(R.compose(R.contains(0), R.keys, R.count_by(Math.floor)))

vf.cells.validator(R.compose(R.equals(0), R.median))

```

## decoupling `slicer_kwargs`

so the idea is to split the part of the validator that defines the validation from the optional part that defines the 'slice' of the dataframe to apply the validator. the latter is the part the uses keyword args `row`, `col`, `filter` to 

while this split definitely makes things more functional, its not clear if this change would be useful or just a step too far. lets consider:

```py

df = pd.Dataframe(...)

slice = vf.frame.slicer(row=[0,1,2], col='net_amount', filter=R.is(Number))

sliced_df = slice(df)

validate_sum_is_zero = vf.cells.validator(R.pipe(R.sum, R.equals(0)))

validate_sum_is_zero(df) # validates all cells in frame 
validate_sum_is_zero(sliced_df)  # validates only cells in slice - slice is duck typing as a df

```

but this doesnt seem to quite gel with how some of the common usecases look. eg. taking an array of validators and apply them all to a single dataframe

so if decoupled, how to we go about pairing validators with slicers?

well we could throw more Ramda at the problem and compose them together

```py

slice_credit = vf.frame.slicer(col='credit', filter=R.is(Number))
slice_debit = vf.frame.slicer(col='debit', filter=R.is(Number))
slice_credit_debit = vf.frame.slicer(col=['credit', 'debit'], filter=R.is(Number))

validators = [
  vf.cells.validator(R.pipe(R.sum, R.equals(0))),
  R.compose(vf.cells.validator(R.pipe(R.sum, R.equals(0))), slice_credit_debit), # sum of all cell values in 'credit' and 'debit' columns is 0
  R.compose(vf.cells.validator(R.all(R.lte(0))), slice_debit), # all cell values in 'debit' column is positive
  R.compose(vf.cells.validator(R.all(R.gte(0))), slice_credit), # all cell values in 'credit' column is negative
  R.compose(vf.cells.validator(R.all(R.both(R.lte(1000), R.gte(10000000)), slice_debit), # all cell values in 'debit' column are between 1,000 and 1 million 
]

# ...

df = pd.Dataframe(...)

# apply each validator to dataframe
for validate in validators:
  validate(df)

```

## feeling out the best way to get it done

its good to remember that we're not stuck with writing everything with Ramda especially if basic python can be terse enough and/or even more expressive:

```py
# all three do the same thing

# ❌ R.lte and R.gte flipped logic still problematic
R.compose(vf.cells.validator(R.all(R.both(R.lte(1000), R.gte(10000000)))), slice_debit) 

# ✅ better
R.compose(vf.cells.validator(R.all(lambda cell : 1000 <= cell and cell <= 1000000)), slice_debit)

# ❌ worse
R.compose(vf.cells.validator(lambda cells : any([1000 <= cell and cell <= 1000000 for cell in cells])), slice_debit)
```

here you can see there's a middle ground where just enough Ramda makes the code better, while too much or too little makes it worse

the other thing not to forget is that there's also that set of predefined validators that handle the most common validations:

```py
# also will the same thing
R.compose(vf.cells.minmax(1000, 10000000), slice_debit) # 🌟 
R.compose(vf.cells.gte(1000), slice_debit) # 🏅 not flipped unlike `R.gte` 
```

obviously those are highly recommended for keeping the code super terse and readable.

in general the [proposed] base validator `vf.cells.validator` comes the most in handy when defining the more cornery validations where you might need to much more Ramda, `lambda` and/or just straight Python to describe more complex pass/fail conditions


## whats your pattern of creating validators?

so heres the very FPy approach:

```py
sum_nums_eq = lambda n : create_validator(R.compose(R.equals(n), R.sum, R.filter(R.is(Number))), "{} must be less than the sum of all number elements".format(n))
sum_nums_eq(0)([1,None,-1]) # true
```

and heres the pythonic kwargsy approach:

```py
sum_nums_eq = lambda n : create_validator(R.equals(n), reducer=R.sum, filter=R.is(Number)), "{} must be less than the sum of all number elements".format(n))
sum_nums_eq(0)([1,None,-1]) # true

# coarser
sum_eq = lambda n, **kwargs : create_validator(R.equals(n), reducer=R.sum, **kwargs), "{} must be less than the sum of all elements".format(n))

# now we can spread in custom filters
sum_eq(0, filter=R.is(Number))([1,None,-1]) # true

sum_nums_eq = lambda n : sum_eq(n, filter=R.is(Number))
sum_nums_eq(0)([1,None,-1]) # true
```

kwargs approach looks more flexible on the surface, but thats kind of a lie as it can be a bit confusing whats really being done with some of the args


## joining validation messages with compose

so how about composing validators, which internally composes their `predicate` and (especially cool) their `fail_msg` values? so we can take a group of these 'validator components' and use them modularly 

```py
filter_nums = V(R.filter(R.is(Number)), "all number elements"
sum_all = V(R.sum, "summed")
eq_zero = V(R.equals(0), "equals 0")
validator = V.pipe(filter_nums, sum_all, eq_zero)

eq = lambda n : V(R.equals(n), "equals {}".format(n))
validator = V.pipe(filter_nums, sum_all, eq(0))

validator.validate([-1000,None,0]) # AssertionError: all number elements summed equals 0


validator = V.pipe(filter_nums, count_all, eq(0))
validator.validate([-1000,None,0]) # AssertionError: all number elements counted equals 0

```

## weird validations

- all in column `'balance'` groupby column `'company'` each summed is between -1 and 1

```py
R.pipe(vf.slice(col=['company', 'balance']), R.groupby()) # oops, need to look at each row, not each cell!

R.pipe(
  vf.rows.slice(col=['company', 'balance']), 
  R.reduceby(lambda acc, row: acc.append(row['balance']), [], R.prop('company')), 
  R.values, 
  R.map(R.sum), 
  R.all(R.both(R.gt(1), R.lt(-1))))

```

you can do it this way with some `lambda`:

```py
R.pipe(
  vf.rows.slicer(col=['company', 'balance']), 
  R.reduceby(lambda acc, row: acc + row['balance'], 0, lambda row: row['company']), 
  R.values, 
  R.all(R.both(R.gt(1), R.lt(-1)))
)
```

lambda acc : lambda row_fn : lambda acc, row: acc + row_fn(row)

R

but also this is how you do it with only Ramda:

```py
is_balanced_enough = R.pipe(
  R.groupBy(R.prop('company')), 
  R.values, 
  R.map(R.map(R.prop('balance'))), # doubly mapped
  R.map(R.sum),
  R.all(R.both(R.gt(1), R.lt(-1)))
)

assert is_balanced_enough(company_balances)

```

this also works:

```py
all_company_balances_summed_close_to_zero = R.pipe(
  R.groupBy(R.prop('company')), 
  R.values, 
  R.map(R.pipe(R.map(R.prop('balance'), R.sum, Math.abs))), # doubly mapped
  R.all(R.both(R.gt(1)))
)
```

heres the imperative pythonic way w/o all the Ramda

```py
def all_company_balances_summed_close_to_zero(rows):
  xs = {}
  for row in rows:
    c = row['company']
    b = row['balance']
    if c in x:
      xs[c] = b   
    else:
      xs[c] += b

  return all([ -1 < x and x < 1 for x in xs.values()])
```


## `Validator` object

```py
vf.cells.sum_eq = lambda n, **kwargs : DfCellsValidator(R.pipe(R.sum, R.equals(n)), "sum equals {}".format(n), **kwargs)

vf.cells.sum_eq(0, cols=['balances'])(df)
```

`DfCellsValidator` internally extracts iterable `cells` from a `df`. then the `predicate` will be applied on the `cells` to say whether it passed or fail

so then you'll also have `DfRowsValidator` and just `DfValidator`

the `validframe` module should provide enough basic ones

```py
import validframe as vf

vf.cells.eq(0, n=atleast(1), cols=['balances']).validate(df)
vf.cells.all_eq(0, cols=['balances']).validate(df)
vf.cells.any_eq(0, cols=['balances']).validate(df)

vf.row_dicts.eq(0)
```

other good names for the function that validates a dataframe:

- `apply`
- `check`
- `validate`
- `call`
- `execute`


## curry quantifiers

on initial thought, having `any_` and `all_` versions of predefined validators seems like a sensible approach in that it provides convenience for developers, esp ones using auto-complete. then drilling deeper into the concept it turns out we'll also need `not_any` and `not_all`.

this could also become an antipattern and source of confusion since it effectively creates different ways to write code that does the thing. 

```py
bloating_validators = [
  vf.cells.all_positive(),
  vf.cells.any_positive(),
  vf.cells.not_all_positive(),
  vf.cells.not_any_positive(),
  vf.cells.positive(quantifier=atleast(3)),
  vf.cells.any_empty(),
  vf.cells.all_empty(col='b', row=[1,2]),
  vf.cells.not_all_empty(col='b', row=[1,2]),
  vf.cells.not_all_not_empty(col=['a','c'], row=[0,3]),
  vf.cells.any_min(0, col=['a','b'], row=3),
  vf.cells.not_any_max(3.14, col=['a','b'], row=3),
  vf.cells.all_minmax(-42, 3.14, filter=R.is(Number)),
  vf.cells.all_min(3.14, col=['a','b'], row=3),
  vf.cells.all_max(0, col=['a','b'], row=3),
  vf.cells.all_minmax(0, 2, filter=R.is(Number)),
  vf.cells.all_ints(col='b'),
  vf.cells.all_floats(col='a'),
  vf.cells.all_strs(row=3), 
  # ...
]
```

the bloat is nice in some ways - for one its more readable than this:

```py
vf.cells.positive(n=not_any)
vf.cells.positive(n=not_all)
vf.cells.positive(n=all)
vf.cells.positive(n=any)
vf.cells.positive(n=atleast(3))
```

this would be crazy:

```py
vf.cells(all).positive()
vf.cells(all, row=3).positive()
vf.cells(all, row=3, filter=R.is(Number)).positive()
vf.cells(not_any, row=3, filter=R.is(Number)).positive()
vf.cells(atleast(3), rows=3, filter=R.is(Number)).positive()
vf.cells(not_any, row=3, filter=R.is(Number)).positive()

```

or better yet:

```py
vf.cells().positive()
vf.cells(all).positive()
vf.cells(any).positive(row=3)
vf.cells(not_all, row=3, filter=R.is(Number)).positive()
vf.cells(not_any).positive(row=3, col='names', filter=R.is(Number))
vf.cells(atleast(3)).positive(row=3, col='names', filter=R.is(Number))
vf.cells(atmost(1)).positive()
```

readable but also a bit weird!

this next one goes all in on readability:

```py
vf.cells(not_all).in_rows(3).filter(R.is(Number)).is_positive()
vf.cells(not_all).in_cols('balance').filter(R.is(Number)).is_positive()
vf.cells_validator(any).in_cols('balance').filter(R.is(Number)).is_positive()
vf.cells_validator(any).in_cols('balance').filter(R.is(Number)).is_minmax(0,10)


some_number_cells_in_col_balances = vf.cells(not_all).filter(R.is(Number)).in_cols('balances')

some_number_cells_in_row_3.total_eq()
some_number_cells_in_row_3.positive()
some_number_cells_in_row_3.negative()


```


### classic classes

```py
FrameValidator(
  R.pipe(frame2cells, R.all(R.eq(0))), # bloated
  'all cells in dataframe must equal 0'
)

CellsValidator(
  R.all(R.eq(0)), # much better
  'all cells in dataframe must equal 0'
)

RowsValidator(
  R.all(lambda row : row['total'] == row['sub_total'] + row['tax']),
  'all rows must have total equal the sub-total plus tax 
)
```