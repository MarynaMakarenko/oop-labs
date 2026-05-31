from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

APARTMENT_CLASSES = ('economy', 'standard', 'luxury')


@dataclass
class Room:
    """A hotel room with its characteristics."""

    id: Optional[int]
    number: str
    capacity: int
    apartment_class: str   # economy | standard | luxury
    price_per_day: float
    is_available: bool = True
    description: str = ''
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'number': self.number,
            'capacity': self.capacity,
            'apartment_class': self.apartment_class,
            'price_per_day': float(self.price_per_day),
            'is_available': self.is_available,
            'description': self.description,
        }
