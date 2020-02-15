def validator(validate_cell, col=None, row=None, filter=None):

  assert callable(validate_cell), 'validate_cell arg must be callable'

  def assert_valid(df, **kwargs): 
    # assert any(df.applymap( ... )
    raise NotImplementedError

  return assert_valid

def positive(**kwargs):
  return validator(lambda x : x > 0, **kwargs)

# or with just lambdas
negative = lambda **kwargs : validator(lambda x: x < 0, **kwargs)