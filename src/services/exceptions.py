class ServiceError(Exception):
    """Base class for all service errors."""


class BookNotFoundError(ServiceError):
    pass


class BookAlreadyExistsError(ServiceError):
    pass


class DatabaseServiceError(ServiceError):
    pass
