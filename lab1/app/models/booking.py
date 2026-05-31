from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

BOOKING_STATUSES = ('pending', 'approved', 'rejected', 'completed')


@dataclass
class Booking:
    """A client's booking request, optionally linked to a room by the admin."""

    id: Optional[int]
    client_id: int
    guests_count: int
    apartment_class: str
    check_in: date
    check_out: date
    status: str = 'pending'
    room_id: Optional[int] = None
    notes: str = ''
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def nights(self) -> int:
        return max((self.check_out - self.check_in).days, 0)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'client_id': self.client_id,
            'room_id': self.room_id,
            'guests_count': self.guests_count,
            'apartment_class': self.apartment_class,
            'check_in': str(self.check_in),
            'check_out': str(self.check_out),
            'status': self.status,
            'notes': self.notes,
            'nights': self.nights,
        }
