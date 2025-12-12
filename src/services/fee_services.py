from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum

"""
Fee management services for the library system.

Handles calculation, tracking, and processing of various library fees
including late fees, replacement fees, and other charges.
"""


class FeeType(Enum):
    """Types of fees that can be charged in the library system."""

    LATE_FEE = "late_fee"
    REPLACEMENT_FEE = "replacement_fee"
    DAMAGE_FEE = "damage_fee"
    PROCESSING_FEE = "processing_fee"
    OVERDUE_FINE = "overdue_fine"


@dataclass
class Fee:
    """Represents a single fee charge."""

    fee_id: str
    member_id: str
    fee_type: FeeType
    amount: float
    description: str
    created_at: datetime
    due_date: datetime
    paid_at: Optional[datetime] = None
    is_paid: bool = False


class FeeCalculator:
    """Calculates various types of library fees."""

    def __init__(self, late_fee_per_day: float = 0.50, max_late_fee: float = 50.0):
        """
        Initialize fee calculator with rates.

        Args:
            late_fee_per_day: Cost per day for overdue items
            max_late_fee: Maximum late fee cap per item
        """
        self.late_fee_per_day = late_fee_per_day
        self.max_late_fee = max_late_fee

    def calculate_late_fee(
        self, due_date: datetime, return_date: Optional[datetime] = None
    ) -> float:
        """
        Calculate late fee based on days overdue.

        Args:
            due_date: Original due date
            return_date: When item was returned (defaults to today)

        Returns:
            Calculated late fee amount
        """
        if return_date is None:
            return_date = datetime.now()

        if return_date <= due_date:
            return 0.0

        days_overdue = (return_date - due_date).days
        fee = days_overdue * self.late_fee_per_day

        return min(fee, self.max_late_fee)

    def calculate_replacement_fee(self, item_value: float) -> float:
        """Calculate replacement fee for lost items."""
        return item_value * 1.1  # 10% markup

    def calculate_damage_fee(
        self, item_value: float, damage_percentage: float = 50.0
    ) -> float:
        """
        Calculate damage fee.

        Args:
            item_value: Original item value
            damage_percentage: Percentage of damage (0-100)

        Returns:
            Damage fee amount
        """
        damage_fraction = min(damage_percentage / 100, 1.0)
        return item_value * damage_fraction


class FeeManager:
    """Manages fee operations and tracking."""

    def __init__(self):
        """Initialize fee manager."""
        self.fees: Dict[str, Fee] = {}
        self.calculator = FeeCalculator()

    def create_fee(
        self,
        member_id: str,
        fee_type: FeeType,
        amount: float,
        description: str,
        due_date_offset_days: int = 30,
    ) -> Fee:
        """
        Create a new fee record.

        Args:
            member_id: Member who incurred the fee
            fee_type: Type of fee
            amount: Fee amount
            description: Fee description
            due_date_offset_days: Days until fee is due

        Returns:
            Created Fee object
        """
        fee_id = f"FEE_{datetime.now().timestamp()}"
        now = datetime.now()

        fee = Fee(
            fee_id=fee_id,
            member_id=member_id,
            fee_type=fee_type,
            amount=amount,
            description=description,
            created_at=now,
            due_date=now + timedelta(days=due_date_offset_days),
        )

        self.fees[fee_id] = fee
        return fee

    def pay_fee(self, fee_id: str) -> bool:
        """
        Mark a fee as paid.

        Args:
            fee_id: ID of fee to pay

        Returns:
            True if successful, False otherwise
        """
        if fee_id not in self.fees:
            return False

        self.fees[fee_id].is_paid = True
        self.fees[fee_id].paid_at = datetime.now()
        return True

    def get_member_fees(self, member_id: str) -> List[Fee]:
        """
        Get all fees for a specific member.

        Args:
            member_id: Member ID to look up

        Returns:
            List of fees for the member
        """
        return [fee for fee in self.fees.values() if fee.member_id == member_id]

    def get_unpaid_fees(self, member_id: str) -> List[Fee]:
        """Get unpaid fees for a member."""
        return [fee for fee in self.get_member_fees(member_id) if not fee.is_paid]

    def calculate_total_owed(self, member_id: str) -> float:
        """Calculate total unpaid fees for a member."""
        return sum(fee.amount for fee in self.get_unpaid_fees(member_id))

    def get_overdue_fees(self) -> List[Fee]:
        """Get all fees past their due date."""
        now = datetime.now()
        return [
            fee for fee in self.fees.values() if not fee.is_paid and fee.due_date < now
        ]
