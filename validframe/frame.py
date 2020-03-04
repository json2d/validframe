def validator(validate_frame, fail_msg=None):
  
  assert callable(validate_frame), "argument 'validate_frame' must be callable"

  def assert_is_valid(df, **kwargs): 
    
    assert validate_frame(df), fail_msg

  return assert_is_valid

def existant():
  return validator(lambda df: df.shape[0] + df.shape[1] > 0, 'df must be existant')

non_existant = lambda : validator(lambda df: df.shape[0] + df.shape[1] > 0, 'df must be non-existant')
