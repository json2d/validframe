from typing import Callable

import ramda as R

from . import core as vf, ramda_ext as R0


PREDICATES = {
    R.equals: "equal to {x}",
    R.is_: "instance of type {x}",
    R.lt: "less than to {x}",
    R.lte: "less than or equal to {x}",
    R.gt: "greater than to {x}",
    R.gte: "greater than or equal to {x}",
}

QUANTIFIERS = {
    R.all: "all",
    R.any: "any",
    R0.some: "some",
    R0.none: "none",
}

REDUCERS = {
    R.sum: "sum",
    R.product: "product",
}

VALIDATORS = {
    vf.CellsValidator: 'cells',
    vf.RowsValidator: 'rows',
}

MSG_TEMPLATE = '{q} of the {v} must be {p} (slice={s})'


def quantitative_validator_factory(validator_type: vf.SliceValidator, quantifier: Callable, predicate: Callable) -> Callable:
  return lambda x, **slice_kwargs: validator_type(
    quantifier(predicate(x)),
    MSG_TEMPLATE.format(s=slice_kwargs, q=QUANTIFIERS[quantifier], v=VALIDATORS[validator_type], p=PREDICATES[predicate].format(x=repr(x))),
    **slice_kwargs
  )


def reductive_validator_factory(validator_type: vf.SliceValidator, reducer: Callable, predicate: Callable) -> Callable:
  return lambda x, **slice_kwargs: validator_type(
    R.compose(predicate(x), reducer),
    MSG_TEMPLATE.format(s=slice_kwargs, q=REDUCERS[reducer], v=VALIDATORS[validator_type], p=PREDICATES[predicate].format(x=repr(x))),
    **slice_kwargs
  )