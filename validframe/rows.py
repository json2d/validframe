import pandas as pd

from . import core as vf, ramda_ext as R0, factory_creators as fc

def uniq(**slice_kwargs):
  # 👀 this validator is actually easier to write with the `FrameValidator` compared to the `RowsValidator` - will they notice?
  return vf.FrameValidator(
    lambda df: len(df[df.duplicated()]) == 0,
    "rows must be unique ({s})".format(s=slice_kwargs),
    **slice_kwargs
  )