def some(predicate): 
  return lambda xs: _uncurried_some(predicate, xs)

def _uncurried_some(predicate, xs):
  # NOTE: performance is best when `xs` is a `<generator>`
  for x in xs: 
    if predicate(x):
      return True
  return False

def none(predicate): 
  return lambda xs: _uncurried_none(predicate, xs)

def _uncurried_none(predicate, xs):
  # NOTE: performance is best when `xs` is a `<generator>`
  for x in xs: 
    if predicate(x):
      return False
  return True