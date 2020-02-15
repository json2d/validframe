def validator(validate_df, fail_msg):
  
  assert callable(validate_df), 'validate_df arg must be callable'

  def assert_valid(df, **kwargs): 
    
    assert validate_df(df), fail_msg

  return assert_valid

def existant():
  return validator(lambda df: df.shape[0] + df.shape[1] > 0, 'df must be existant')

non_existant = lambda : validator(lambda df: df.shape[0] + df.shape[1] > 0, 'df must be non-existant')
