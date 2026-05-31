import logging
from typing import List, Optional

from app.core.database import db
from app.dao.base_dao import BaseDAO
from app.models.room import Room

logger = logging.getLogger(__name__)


class RoomDAO(BaseDAO):
    table = 'rooms'

    def _map(self, row) -> Optional[Room]:
        if row is None:
            return None
        return Room(
            id=row['id'],
            number=row['number'],
            capacity=row['capacity'],
            apartment_class=row['apartment_class'],
            price_per_day=float(row['price_per_day']),
            is_available=row['is_available'],
            description=row['description'] or '',
            created_at=row['created_at'],
        )

    def find_by_id(self, room_id: int) -> Optional[Room]:
        return self._map(super().find_by_id(room_id))

    def find_all(self) -> List[Room]:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM rooms ORDER BY number')
            return [self._map(r) for r in cur.fetchall()]

    def find_available(self, guests: int, apartment_class: str) -> List[Room]:
        with db.cursor() as cur:
            cur.execute(
                '''SELECT * FROM rooms
                   WHERE is_available = TRUE AND capacity >= %s AND apartment_class = %s
                   ORDER BY price_per_day''',
                (guests, apartment_class),
            )
            return [self._map(r) for r in cur.fetchall()]

    def create(self, number: str, capacity: int, apartment_class: str,
               price_per_day: float, description: str = '') -> Room:
        with db.cursor() as cur:
            cur.execute(
                '''INSERT INTO rooms (number, capacity, apartment_class, price_per_day, description)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id''',
                (number, capacity, apartment_class, price_per_day, description),
            )
            room_id = cur.fetchone()[0]
        logger.info("Created room %s id=%s", number, room_id)
        return self.find_by_id(room_id)

    def update(self, room_id: int, **kwargs) -> Optional[Room]:
        allowed = {'number', 'capacity', 'apartment_class', 'price_per_day',
                   'is_available', 'description'}
        fields = {k: v for k, v in kwargs.items() if k in allowed}
        if not fields:
            return self.find_by_id(room_id)
        set_clause = ', '.join(f'{k} = %s' for k in fields)
        with db.cursor() as cur:
            cur.execute(
                f'UPDATE rooms SET {set_clause} WHERE id = %s',
                list(fields.values()) + [room_id],
            )
        logger.info("Updated room id=%s", room_id)
        return self.find_by_id(room_id)

    def set_availability(self, room_id: int, available: bool) -> None:
        with db.cursor() as cur:
            cur.execute(
                'UPDATE rooms SET is_available = %s WHERE id = %s',
                (available, room_id),
            )
