class ServiceError(Exception):
    """Base class for all service errors."""


class DatabaseServiceError(ServiceError):
    pass


class InvalidEmailError(ServiceError):
    pass
