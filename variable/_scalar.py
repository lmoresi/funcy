from numbers import Number, Real, Integral

from ..special import null
from ._number import Number

class Scalar(Number):

    def __init__(self,
            arg,
            /,
            *args,
            **kwargs,
            ):
        if type(arg) is type:
            if issubclass(arg, Real):
                super().__init__(arg, *args, **kwargs,)
            else:
                raise TypeError(arg)
        elif isinstance(arg, Real):
            super().__init__(type(arg), *args, **kwargs,)
            self.data = arg
        else:
            raise TypeError(type(arg))

    def set(self, val):
        self.data = val
        self.refresh()
    def rectify(self):
        self.data = self.dtype(self.data)
    def nullify(self):
        self.data = null
        self.refresh()

    @property
    def isnull(self):
        return self.data is null
