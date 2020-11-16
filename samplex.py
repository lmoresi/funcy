from ._fn import Fn

class Seqx:
    def __init__(self, **kwargs):
        self._dict = OrderedDict(
            (k, Fn(v)) for k, v in kwargs.items()
            )
