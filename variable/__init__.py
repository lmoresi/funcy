from ._base import Variable
from ._scalar import Scalar
from ._array import Array

def construct_variable(*args, **kwargs):
    totry = Scalar, Array
    for kind in totry:
        try:
            return kind(*args, **kwargs)
        except TypeError:
            pass
    raise TypeError
Variable.construct_variable = construct_variable
