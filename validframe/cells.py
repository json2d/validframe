import ramda as R

from . import core as vf, ramda_ext as R0, factory_creators as fc

# curry down factory creators for vf.CellsValidator type
qv_factory = lambda quantifier, predicate: fc.quantitative_validator_factory(vf.CellsValidator, quantifier, predicate)
rv_factory = lambda reducer, predicate: fc.reductive_validator_factory(vf.CellsValidator, reducer, predicate)

all_is = qv_factory(R.all, R.is_) 
all_eq = qv_factory(R.all, R.equals)       
all_gt = qv_factory(R.all, R.gt) 
all_lt = qv_factory(R.all, R.lt) 
all_gte = qv_factory(R.all, R.gte) 
all_lte = qv_factory(R.all, R.lte) 

some_is = qv_factory(R0.some, R.is_) 
some_eq = qv_factory(R0.some, R.equals)       
some_gt = qv_factory(R0.some, R.gt) 
some_lt = qv_factory(R0.some, R.lt) 
some_gte = qv_factory(R0.some, R.gte) 
some_lte = qv_factory(R0.some, R.lte) 

none_is = qv_factory(R.none, R.is_) 
none_eq = qv_factory(R.none, R.equals)       
none_gt = qv_factory(R.none, R.gt) 
none_lt = qv_factory(R.none, R.lt) 
none_gte = qv_factory(R.none, R.gte) 
none_lte = qv_factory(R.none, R.lte) 

all_or_some_is = qv_factory(R0.all_or_some, R.is_) 
all_or_some_eq = qv_factory(R0.all_or_some, R.equals)       
all_or_some_gt = qv_factory(R0.all_or_some, R.gt) 
all_or_some_lt = qv_factory(R0.all_or_some, R.lt) 
all_or_some_gte = qv_factory(R0.all_or_some, R.gte) 
all_or_some_lte = qv_factory(R0.all_or_some, R.lte) 

some_or_none_is = qv_factory(R0.some_or_none, R.is_) 
some_or_none_eq = qv_factory(R0.some_or_none, R.equals)       
some_or_none_gt = qv_factory(R0.some_or_none, R.gt) 
some_or_none_lt = qv_factory(R0.some_or_none, R.lt) 
some_or_none_gte = qv_factory(R0.some_or_none, R.gte) 
some_or_none_lte = qv_factory(R0.some_or_none, R.lte) 

all_or_none_is = qv_factory(R0.all_or_none, R.is_) 
all_or_none_eq = qv_factory(R0.all_or_none, R.equals)       
all_or_none_gt = qv_factory(R0.all_or_none, R.gt) 
all_or_none_lt = qv_factory(R0.all_or_none, R.lt) 
all_or_none_gte = qv_factory(R0.all_or_none, R.gte) 
all_or_none_lte = qv_factory(R0.all_or_none, R.lte) 

sum_is = rv_factory(R.sum, R.is_)
sum_eq = rv_factory(R.sum, R.equals)
sum_gt = rv_factory(R.sum, R.gt)
sum_lt = rv_factory(R.sum, R.lt)
sum_gte = rv_factory(R.sum, R.gte)
sum_lte = rv_factory(R.sum, R.lte)
