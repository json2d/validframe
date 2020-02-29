import validium as V

class SliceValidator(V.Validator):
  def __init__(self, predicate, fail_msg=None, cols=None, rows=None):
    super().__init__(predicate, fail_msg)
    
    self.cols = cols
    self.rows = rows

class FrameValidator(SliceValidator):
  def validate(self, df):
    if self.rows is None and self.cols is None:
      sliced_df = df
    elif self.rows is None:
      sliced_df = df.loc[self.rows]
    elif self.cols is None:
      sliced_df = df[self.cols]
    else: # self.rows and self.cols not None
      sliced_df = df.loc[self.rows, self.cols]

    super().validate(sliced_df)

class CellsValidator(SliceValidator):
  def validate(self, df):
    cells = CellsValidator.iter_cells(df, self.cols, self.rows)
    super().validate(cells)

  @staticmethod
  def iter_cells(df, cols=None, rows=None):
    rows_slice = range(len(df)) if rows is None else rows
    cols_slice = df.columns if cols is None else cols

    for row_idx in rows_slice: 
      for col_name in cols_slice:
        yield df.loc[row_idx, col_name]

class RowsValidator(V.Validator):

  def validate(self, df):
    rows = df.iterrows()
    super().validate(rows)
