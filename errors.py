class UserDefinedExceptions(Exception):
    pass


class UndefinedObjectException(UserDefinedExceptions):
    def __init__(self, msg):
        super().__init__(msg,)
        print(msg)


class ConnectionFailed(UserDefinedExceptions):
    def __init__(self, msg):
        super().__init__(msg,)
        print(msg)
