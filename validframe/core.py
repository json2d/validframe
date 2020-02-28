import validium as V

class FrameValidator(V.Validator):
  pass

class CellsValidator(V.Validator):

  def __init__(self, predicate, fail_msg=None, cols=None, rows=None):

    super().__init__(predicate, fail_msg)
    
    self.cols = cols
    self.rows = rows

  def validate(self, df):
    cells = CellsValidator.iter_cells(df, self.cols, self.rows)
    super().validate(cells)

  @staticmethod
  def iter_cells(df, cols=None, rows=None):
    raise NotImplementedError

class RowsValidator(V.Validator):

  def validate(self, df):
    rows = df.iterrows()
    super().validate(rows)
