from flask import current_app
import traceback

class HTTPException(Exception):
    def __init__(self, message=None):
        super().__init__(message)
        current_app.logger.error(traceback.format_exc())

class NotFoundError(HTTPException):
    pass

class AlreadyExistsError(HTTPException):
    pass

class BadInputError(HTTPException):
    pass

class TokenInvalidError(HTTPException):
    pass