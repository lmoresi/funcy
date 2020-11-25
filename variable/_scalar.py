from numbers import Number, Real, Integral

from ._simple import Simple

class Scalar(Simple):

    __slots__ = (
        'dtype',
        )

    def __init__(self,
            arg,
            ):
        if type(arg) is type:
            if issubclass(arg, Real):
                self.dtype = arg
                initialValue = None
            else:
                raise TypeError(arg)
        elif isinstance(arg, Real):
            self.dtype = type(arg)
            initialValue = arg
        else:
            raise TypeError(type(arg))
        super().__init__(self.dtype, initialValue = initialValue)

    def _rectify(self):
        self.data = self.dtype(self.data)
