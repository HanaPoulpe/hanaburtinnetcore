class OperationError(RuntimeError):
    def __init__(self, operation_name: str, message: str) -> None:
        self.operation_name = operation_name
        self.message = message
        super().__init__(operation_name, message)

    def __repr__(self) -> str:
        return "%(class_name)s<%(operation_name)s>(%(message)r)" % {
            "class_name": self.__class__.__name__,
            "operation_name": self.operation_name,
            "message": self.message,
        }
