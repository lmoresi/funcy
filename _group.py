from ._base import Function

class Group(Function):
    def _operate(self, *args, op = None, truthy = False, **kwargs):
        return Operation(*[*self, *args], op = op, **kwargs)
    def _evaluate(self):
        return iter(self)

from ._operation import Operation
