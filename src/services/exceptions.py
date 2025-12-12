class ServiceError(Exception):
    """Base class for all service errors."""


# BookExceptions
class BookNotFoundError(ServiceError):
    pass


class BookAlreadyExistsError(ServiceError):
    pass


class InvalidBookData(ServiceError):
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


# FeeExceptions
class FeeNotFoundError(ServiceError):
    pass


class FeeCalculationError(ServiceError):
    pass


class PaymentProcessingError(ServiceError):
    pass


# NotificationExceptions
class NotificationNotFoundError(ServiceError):
    pass


class NotificationDeliveryError(ServiceError):
    pass


# DatabaseExceptions
class DatabaseServiceError(ServiceError):
    pass


class TransactionError(ServiceError):
    pass
