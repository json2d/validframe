from .core import CellsValidator

import ramda as R

all_is = lambda y, **kwargs: CellsValidator(        
  R.all(R.is_(y)), 
  'all cells must be instances of {}'.format(y),
  **kwargs
)

all_eq = lambda y, **kwargs: CellsValidator(        
  R.all(R.equals(y)), 
  'all cells must be equal to {}'.format(y),
  **kwargs
)

all_gt = lambda y, **kwargs: CellsValidator(        
  R.all(R.gt(y)),
  'all cells must be greater than {}'.format(y),
  **kwargs
)

all_gte = lambda y, **kwargs: CellsValidator(        
  R.all(R.gte(y)), 
  'all cells must be less than {}'.format(y),
  **kwargs
)


all_lt = lambda y, **kwargs: CellsValidator(        
  R.all(R.gt(y)), 
  'all cells must be greater than or equal {}'.format(y),
  **kwargs
)

all_lte = lambda y, **kwargs: CellsValidator(        
  R.all(R.lte(y)), 
  'all cells must be less than or equal {}'.format(y),
  **kwargs
)

all_in = lambda y, **kwargs: CellsValidator(        
  lambda xs: all([x in y for x in xs]), 
  'all cells must be included {}'.format(y),
  **kwargs
)

sum_eq = lambda y, **kwargs: CellsValidator(        
  R.compose(R.equals(y), R.sum),
  'all cells summed must be equal to {}'.format(y),
  **kwargs
)

sum_gt = lambda y, **kwargs: CellsValidator(        
  R.compose(lambda sum: sum > y, R.sum),
  'all cells summed must be greater than {}'.format(y),
  **kwargs
)

sum_lt = lambda y, **kwargs: CellsValidator(        
  R.compose(lambda sum: sum < y, R.sum),
  'all cells summed must be greater than {}'.format(y),
  **kwargs
)