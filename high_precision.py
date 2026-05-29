from __future__ import annotations
import math
from decimal import Decimal, getcontext, localcontext
from typing import Union
getcontext().prec = 60
Number = Union[float, Decimal]
def to_decimal(x: Number) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))
def sqrt(x: Number) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = getcontext().prec
        return to_decimal(x).sqrt()
def exp(x: Number) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = getcontext().prec
        return to_decimal(x).exp()
def log(x: Number, base: Number = math.e) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = getcontext().prec
        d = to_decimal(x).ln()
        return d / to_decimal(base).ln() if base != math.e else d
