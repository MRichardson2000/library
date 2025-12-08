from dataclasses import dataclass
from datetime import date


@dataclass
class Loan:
    loan_id: int
    user_id: int
    book_id: int
    loan_date: date
    due_date: date
    returned: bool = False
