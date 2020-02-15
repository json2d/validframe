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

## pedal to the metal using Ramda

```py
import ramda as R

vf.cells.validator(R.gte(0))
vf.cells.validator(R.equals(0))

vf.cells.validator(R.equals(111), filter=R.gt(0))

vf.cells.validator(R.equals(111), n=R.all(R.identity))
vf.cells.validator(R.equals(111), n=atleast(3)) # not sure how you could do this one with Ramda

vf.cells.validator(R.either(R.equals(111),R.equals(-100)))
```