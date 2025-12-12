class ServiceError(Exception):
    """Base class for all service errors."""


# BookExceptions
class BookNotFoundError(ServiceError):
    pass


class BookAlreadyExistsError(ServiceError):
    pass


# UserExceptions
class UserAlreadyExistsError(ServiceError):
    pass


class UserNotFoundError(ServiceError):
    pass


class InvalidEmailError(ServiceError):
    pass


# LoanExceptions
class LoanNotFoundError(ServiceError):
    pass


class LoanAlreadyExistsError(ServiceError):
    pass


class LoanLimitExceededError(ServiceError):
    pass


class LoanOverdueError(ServiceError):
    pass


# InventoryExceptions
class InventoryNotFoundError(ServiceError):
    pass


class InventoryUpdateError(ServiceError):
    pass


# DatabaseExceptions
class DatabaseServiceError(ServiceError):
    pass
