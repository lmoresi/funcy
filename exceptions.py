class FunctionException(Exception):
    pass

class MissingAsset(FunctionException):
    pass

class NullValueDetected(FunctionException):
    pass
class InfiniteValueDetected(FunctionException):
    pass

class EvaluationError(FunctionException):
    pass

class NotYetImplemented(Exception):
    pass

class RedundantConvert(FunctionException):
    pass

class CannotProcess(FunctionException):
    pass

class CannotDetermineDataType(FunctionException):
    pass

class ClosureExceptions(FunctionException):
    pass
class NothingToClose(ClosureExceptions):
    pass

class FunctionCreationException(FunctionException):
    pass
