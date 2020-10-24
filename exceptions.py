class FunctionException(Exception):
    pass

class MissingAsset(FunctionException):
    pass

class FunctionMissingAsset(MissingAsset, FunctionException):
    pass
class NullValueDetected(FunctionException):
    pass
class EvaluationError(FunctionException):
    pass

class NotYetImplemented(Exception):
    pass
