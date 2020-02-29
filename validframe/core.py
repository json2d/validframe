import validium as V

class SliceValidator(V.Validator):
  def __init__(self, predicate, fail_msg=None, cols=None, rows=None):
    super().__init__(predicate, fail_msg)
    
    self.cols = cols
    self.rows = rows
  
  def validate(self, target):
    super().validate(target)
    # print('passed:', self.fail_msg)

  def slice(self, df):
    if self.rows is None and self.cols is None:
      sliced_df = df
    elif self.rows is None and self.cols is not None:
      sliced_df = df[self.cols]
    elif self.rows is not None and self.cols is None:
      sliced_df = df.loc[self.rows]
    else: # self.rows and self.cols not None
      sliced_df = df.loc[self.rows, self.cols]
    return sliced_df

class FrameValidator(SliceValidator):
  def validate(self, df):
    super().validate(self.slice(df))

class CellsValidator(SliceValidator):
  def validate(self, df):
    cells = CellsValidator.iter_cells(self.slice(df))
    super().validate(cells)

  @staticmethod
  def iter_cells(df):
    cols = df.columns
    for row_idx, row in df.iterrows(): 
      for col_name in cols:
        yield df.loc[row_idx, col_name]

class RowsValidator(SliceValidator):
  def validate(self, df):
    rows = self.slice(df).iterrows()
    super().validate(rows)
