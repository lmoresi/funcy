from ._base import Function
from .exceptions import *

class Thing(Function):
    def __init__(self, thing, **kwargs):
        self.thing = thing
        super().__init__(**kwargs)
    def _evaluate(self):
        return self.thing
