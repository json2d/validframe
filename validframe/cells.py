import ramda as R

from . import core as vf, factory_creators as fc

# curry down factory creators for vf.CellsValidator type
qv_factory = lambda quantifier, predicate: fc.quantitative_validator_factory(vf.CellsValidator, quantifier, predicate)
rv_factory = lambda reducer, predicate: fc.reductive_validator_factory(vf.CellsValidator, reducer, predicate)

all_is = qv_factory(R.all, R.is_) 
all_eq = qv_factory(R.all, R.equals)       
all_gt = qv_factory(R.all, R.gt) 
all_lt = qv_factory(R.all, R.lt) 
all_gte = qv_factory(R.all, R.gte) 
all_lte = qv_factory(R.all, R.lte) 

sum_is = rv_factory(R.sum, R.is_)
sum_eq = rv_factory(R.sum, R.equals)
sum_gt = rv_factory(R.sum, R.gt)
sum_lt = rv_factory(R.sum, R.lt)
sum_gte = rv_factory(R.sum, R.gte)
sum_lte = rv_factory(R.sum, R.lte)
