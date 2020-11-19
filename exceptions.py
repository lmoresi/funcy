class FuncyException(Exception):
    pass

class MissingAsset(FuncyException):
    pass

class NullValueDetected(FuncyException):
    pass
class InfiniteValueDetected(FuncyException):
    pass

class EvaluationError(FuncyException):
    pass

class NotYetImplemented(Exception):
    pass

class RedundantConvert(FuncyException):
    pass

class CannotProcess(FuncyException):
    pass

class CannotDetermineDataType(FuncyException):
    pass

class ClosureExceptions(FuncyException):
    pass
class NothingToClose(ClosureExceptions):
    pass
