from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

INVOICE_STATUSES = ('unpaid', 'paid')


@dataclass
class Invoice:
    """A financial invoice issued after a booking is approved."""

    id: Optional[int]
    booking_id: int
    amount: float
    status: str = 'unpaid'
    issued_at: datetime = field(default_factory=datetime.now)
    paid_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'amount': float(self.amount),
            'status': self.status,
            'issued_at': str(self.issued_at),
            'paid_at': str(self.paid_at) if self.paid_at else None,
        }
