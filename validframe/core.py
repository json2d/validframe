import validium as V

def slice(df, rows = None, cols = None):
  if rows is None and cols is None:
    sliced_df = df
  elif rows is None and cols is not None:
    sliced_df = df[cols]
  elif rows is not None and cols is None:
    sliced_df = df.loc[rows]
  else: # both rows and cols is not None
    sliced_df = df.loc[rows, cols]
  return sliced_df
  
def itercells(df):
  cols = df.columns
  for row_idx, row in df.iterrows(): 
    for col_name in cols:
      yield df.loc[row_idx, col_name]

def iterrows(df):
  for row_idx, row in df.iterrows(): 
    yield row # 👃 drop row_idx parameter - if needed can use FrameValidator instead of RowsValidator 
        
class SliceValidator(object):
  def __init__(self, predicate, fail_msg=None, cols=None, rows=None):
    self.cols = cols
    self.rows = rows
    self._v = V.Validator(predicate, fail_msg)

class FrameValidator(SliceValidator):
  def validate(self, df, **kwargs):
    sliced_df = slice(df, self.rows, self.cols)
    self._v.validate(sliced_df, **kwargs)

  def confirm(self, df, **kwargs):
    sliced_df = slice(df, self.rows, self.cols)
    return self._v.confirm(sliced_df, **kwargs) 

class CellsValidator(SliceValidator):
  def validate(self, df, **kwargs):
    sliced_df = slice(df, self.rows, self.cols)
    cells = itercells(sliced_df)
    self._v.validate(cells, **kwargs)

  def confirm(self, df, **kwargs):
    sliced_df = slice(df, self.rows, self.cols)
    cells = itercells(sliced_df)
    return self._v.confirm(cells, **kwargs)

class RowsValidator(SliceValidator):
  def validate(self, df, **kwargs):
    sliced_df = slice(df, self.rows, self.cols)
    rows = iterrows(sliced_df)
    self._v.validate(rows, **kwargs)

  def confirm(self, df, **kwargs):
    sliced_df = slice(df, self.rows, self.cols)
    rows = iterrows(sliced_df)
    return self._v.confirm(rows, **kwargs)
