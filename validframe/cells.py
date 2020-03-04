def validator(validate_cell, fail_msg=None, col=None, row=None, filter=None):

  assert callable(validate_cell), "argument 'validate_cell' must be callable"

  def assert_is_valid(df, **kwargs): 
    # assert any( ... )
    raise NotImplementedError

  return assert_is_valid

def positive(**kwargs):
  return validator(
    validate_cell=lambda x : x > 0, 
    fail_msg="cells should be positive",
    **kwargs
  )

# or with just lambdas
negative = lambda **kwargs : validator(lambda x: x < 0, "cells should be negative", **kwargs)