import ramda as R

def some(predicate): 
  return lambda xs: _uncurried_some(predicate, xs)

def _uncurried_some(predicate, xs):
  trend = None
  for x in xs: 
    cur = predicate(x)
    if trend is None:
      trend = cur
    elif not cur == trend: # atleast 1 pass and 1 fail
      return True

  return False # all pass or all fail

def all_or_some(predicate): 
  return lambda xs: not R.none(predicate)(xs)

def some_or_none(predicate): 
  return lambda xs: not R.all(predicate)(xs)

def all_or_none(predicate): 
  return lambda xs: not some(predicate)(xs)
