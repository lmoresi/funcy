from ._base import Function
from .exceptions import *

class Thing(Function):
    def __init__(self, thing):
        self.thing = thing
        super().__init__(thing)
    def _evaluate(self):
        return self.thing
