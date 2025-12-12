from enum import Enum


class LoanStatus(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    RETURNED = "Returned"
    OVERDUE = "Overdue"


class AccountState(Enum):
    ACTIVE = "Active"
    DELETED = "Deleted"
    SUSPENDED = "Suspended"
