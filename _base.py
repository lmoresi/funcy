from wordhash import w_hash

from .exceptions import *

def convert(arg):
    try:
        return Function(arg)
    except RedundantConvert:
        return arg

class Function:

    def __new__(cls, *args, **kwargs):
        if cls is Function:
            if len(args) == 0:
                cls = Slot
            elif len(args) > 1:
                cls = Seq
            else:
                arg = args[0]
                if len(kwargs) == 0 and isinstance(arg, Function):
                    raise RedundantConvert
                check = Variable._check_arg(arg)
                if check is None:
                    cls = Thing
                else:
                    cls = FixedVariable
        obj = super().__new__(cls)
        return obj

    def __init__(self, *terms, **kwargs):
        # self.terms = [convert(t) for t in terms]
        self.terms = terms
        if len(terms) == 1:
            self.arg = terms[0]
        else:
            self.arg = terms
        self.kwargs = kwargs
        # super().__init__(*self.args, **self.kwargs)

    @staticmethod
    def _value_resolve(val):
        while isinstance(val, Function):
            val = val.value
        return val
    def evaluate(self):
        if self.open:
            raise EvaluationError("Cannot evaluate open function.")
        else:
            val = self._evaluate()
            val = self._value_resolve(val)
            return val
    def _evaluate(self):
        raise MissingAsset
    @property
    def value(self):
        return self.evaluate()
    @property
    def null(self):
        return self._isnull()
    def _isnull(self):
        return False
    @property
    def name(self):
        if not hasattr(self, '_name'):
            return None
        return str(self._name)

    def _count_slots(self):
        terms = self.terms
        argslots = 0
        kwargslots = []
        for term in terms:
            if isinstance(term, Function):
                if type(term) is Slot:
                    if term.argslots:
                        argslots += 1
                    elif not term.name in kwargslots:
                        kwargslots.append(term.name)
                else:
                    kwargslots.extend(
                        k for k in term.kwargslots if not k in kwargslots
                        )
                    argslots += term.argslots
        return argslots, kwargslots
    def _add_slot_attrs(self):
        if not '_slots' in dir(self):
            self._argslots, self._kwargslots = self._count_slots()
            self._slots = self._argslots + len(self._kwargslots)
        else:
            pass
    @property
    def slots(self):
        self._add_slot_attrs()
        return self._slots
    @property
    def argslots(self):
        self._add_slot_attrs()
        return self._argslots
    @property
    def kwargslots(self):
        self._add_slot_attrs()
        return self._kwargslots
    @property
    def open(self):
        return bool(self.slots)
    def allclose(self, arg):
        target = self
        while target.open:
            target = target.close(arg)
        assert not target.open
        return target
    def close(self,
            *queryArgs,
            **queryKwargs
            ):
        badKeys = [k for k in queryKwargs if not k in self.kwargslots]
        if badKeys:
            raise FunctionException("Inappropriate kwargs:", badKeys)
        unmatchedKwargs = [k for k in self.kwargslots if not k in queryKwargs]
        if len(queryArgs) > self.argslots and len(unmatchedKwargs):
            excessArgs = queryArgs[-(len(queryArgs) - self.argslots):]
            extraKwargs = dict(zip(self.kwargslots, excessArgs))
            excessArgs = excessArgs[len(extraKwargs):]
            if len(excessArgs):
                raise FunctionException("Too many args:", excessArgs)
            queryKwargs.update(extraKwargs)
        queryArgs = iter(queryArgs[:self.argslots])
        terms = []
        changes = 0
        for t in self.terms:
            if type(t) is Slot:
                if t.argslots:
                    try:
                        t = next(queryArgs)
                        changes += 1
                    except StopIteration:
                        pass
                else:
                    if t.name in queryKwargs:
                        t = queryKwargs[t.name]
                        changes += 1
            elif isinstance(t, Function):
                if t.open:
                    queryArgs = list(queryArgs)
                    subArgs = queryArgs[:t.argslots]
                    leftovers = queryArgs[t.argslots:]
                    subKwargs = {
                        k: queryKwargs[k]
                            for k in queryKwargs if k in t.kwargslots
                        }
                    t = t.close(
                        *subArgs,
                        **subKwargs,
                        )
                    changes += 1
                    queryArgs = iter(leftovers)
            terms.append(t)
        if changes:
            outObj = type(self)(*terms, **self.kwargs)
        else:
            outObj = self
        return outObj

    def _operate(self, *args, op = None, truthy = False, **kwargs):
        return Operation(self, *args, op = op, **kwargs)

    def __eq__(self, *args):
        return self._operate(*args, op = 'eq', truthy = True)
    def __ne__(self, *args):
        return self._operate(*args, op = 'ne', truthy = True)
    def __ge__(self, *args):
        return self._operate(*args, op = 'ge', truthy = True)
    def __le__(self, *args):
        return self._operate(*args, op = 'le', truthy = True)
    def __gt__(self, *args):
        return self._operate(*args, op = 'gt', truthy = True)
    def __lt__(self, *args):
        return self._operate(*args, op = 'lt', truthy = True)
    def __and__(self, *args):
        return self._operate(*args, op = 'all', truthy = True)
    def __or__(self, *args):
        return self._operate(*args, op = 'any', truthy = True)
    def __invert__(self, *args):
        return self._operate(*args, op = 'not', truthy = True)
    def __add__(self, *args):
        return self._operate(*args, op = 'add')
    def __floordiv__(self, *args):
        return self._operate(*args, op = 'floordiv')
    def __truediv__(self, *args):
        return self._operate(*args, op = 'truediv')
    def __mod__(self, *args):
        return self._operate(*args, op = 'mod')
    def __mul__(self, *args):
        return self._operate(*args, op = 'mul')
    def __pow__(self, *args):
        return self._operate(*args, op = 'pow')
    def __sub__(self, *args):
        return self._operate(*args, op = 'sub')
    def __truediv__(self, *args):
        return self._operate(*args, op = 'truediv')
    def __neg__(self, *args):
        return self._operate(*args, op = 'neg')

    def _reassign(self, arg, op = None):
        return self._operate(arg, op = op)

    def __iadd__(self, arg): return self._reassign(arg, op = 'add')
    def __ifloordiv__(self, arg): return self._reassign(arg, op = 'floordiv')
    def __imod__(self, arg): return self._reassign(arg, op = 'mod')
    def __imul__(self, arg): return self._reassign(arg, op = 'mul')
    def __ipow__(self, arg): return self._reassign(arg, op = 'pow')
    def __isub__(self, arg): return self._reassign(arg, op = 'sub')
    def __itruediv__(self, arg): return self._reassign(arg, op = 'truediv')

    def __bool__(self):
        try:
            return bool(self.value)
        except NullValueDetected:
            return False
    # @staticmethod
    # def bool(arg):
    #     return Operation(*args, op = bool)
    # @staticmethod
    # def all(*args):
    #     return Operation(*args, op = all)
    # @staticmethod
    # def any(*args):
    #     return Operation(*args, op = any)
    # @staticmethod
    # def not_fn(*args):
    #     return Operation(*args, op = bool, invert = True)

    def pipe_out(self, arg):
        if type(arg) is list:
            try:
                arg = arg[0]
            except IndexError:
                arg = None
            outcls = ExtendableVariable
        else:
            outcls = FixedVariable
        arg = convert(arg)
        if not isinstance(arg, FixedVariable):
            raise FunctionException(arg)
        return outcls(self, **arg.kwargs)
    def __rshift__(self, arg):
        return self.pipe_out(arg)
    def __lshift__(self, arg):
        return arg.pipe_out(self)

    @property
    def namestr(self):
        return self._namestr()
    def _namestr(self):
        out = type(self).__name__ + self.kwargstr
        termstr = lambda t: t.namestr if hasattr(t, 'namestr') else str(t)
        if len(self.terms):
            termstr = ', '.join(termstr(t) for t in self.terms)
            out += '(' + termstr + ')'
        return out
    @property
    def kwargstr(self):
        return self._kwargstr()
    def _kwargstr(self):
        outs = []
        for key, val in sorted(self.kwargs.items()):
            if not type(val) is str:
                if isinstance(val, Function):
                    val = val.namestr
                else:
                    try:
                        val = val.__name__
                    except AttributeError:
                        val = str(val)
            outs.append(': '.join((key, val)))
        return '{' + ', '.join(outs) + '}'

    @property
    def valstr(self):
        return self._valstr()
    def _valstr(self):
        if self.open:
            return 'open:' + str((self.argslots, self.kwargslots))
        else:
            try:
                return str(self.value)
            except (NullValueDetected, EvaluationError):
                return 'Null'
    def __repr__(self):
        return self.namestr
    def __str__(self):
        return ' == '.join([self.namestr, self.valstr])
    @property
    def hashID(self):
        return w_hash(self.namestr)

    def __call__(self, *args, **kwargs):
        if len(args) or len(kwargs):
            self = self.close(*args, **kwargs)
        return self.evaluate()

    @property
    def get(self):
        return Getter(self)
    def __getitem__(self, key):
        return self.value[key]

    def op(self, arg, **kwargs):
        return Operation(self, op = arg, **kwargs)

    def exc(self, exc = Exception, altVal = None):
        return Trier(self, exc = exc, altVal = altVal)

class Getter:
    def __init__(self, host):
        self.host = host
    def __call__(self, *args):
        return self.__getattr__(*args)
    def __getattr__(self, *keys):
        return Function(self.host, *keys).reduce(getattr)
    def __getitem__(self, arg):
        if type(arg) is tuple:
            return Function(self.host, *arg).reduce('getitem')
        else:
            return Function(self.host, arg).op('getitem')

from ._operation import Operation #, Boolean
from ._trier import Trier
from ._seq import Seq
from ._variable import Variable, FixedVariable, ExtendableVariable
from ._thing import Thing
from ._slot import Slot
