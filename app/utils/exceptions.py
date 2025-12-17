class AppError(Exception):
    """
    Custom exception class for application errors.

    This exception is designed to handle errors in the application, providing a message,
    an optional HTTP status code (defaulting to 400 for bad requests), and an optional
    payload for additional error details (e.g., for API responses).

    Attributes:
        message (str): The error message.
        status_code (int): The HTTP status code associated with the error (default: 400).
        payload (dict, optional): Additional data to include with the error (default: None).
    """

    def __init__(self, message, status_code=400, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload


class ResourceNotFound(AppError):
    def __init__(self, message="Resource not found", status_code=404, payload=None):
        super().__init__(message, status_code, payload)


class ResourceAlreadyExists(AppError):
    def __init__(
        self, message="Resource already exists", status_code=409, payload=None
    ):
        super().__init__(message, status_code, payload)


class AuthenticationError(AppError):
    def __init__(self, message="Authentication failed", status_code=401, payload=None):
        super().__init__(message, status_code, payload)


class CreationError(AppError):
    def __init__(
        self, message="Failed to create resource", status_code=400, payload=None
    ):
        super().__init__(message, status_code, payload)
