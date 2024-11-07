class CustomError(Exception):
    pass

class NotFoundError(CustomError):
    pass

class AlreadyExistsError(CustomError):
    pass

class BadInputError(CustomError):
    pass

class TokenInvalidError(CustomError):
    pass