from ._base import Variable
from ._simple import Simple
from ._scalar import Scalar

def construct_variable(*args, **kwargs):
    totry = Scalar, #Array
    for kind in totry:
        try:
            return kind(*args, **kwargs)
        except TypeError:
            pass
    raise TypeError
Variable.construct_variable = construct_variable
