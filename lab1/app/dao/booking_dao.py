import logging
from typing import List, Optional

from app.core.database import db
from app.dao.base_dao import BaseDAO
from app.models.booking import Booking

logger = logging.getLogger(__name__)


class BookingDAO(BaseDAO):
    table = 'bookings'

    def _map(self, row) -> Optional[Booking]:
        if row is None:
            return None
        return Booking(
            id=row['id'],
            client_id=row['client_id'],
            room_id=row['room_id'],
            guests_count=row['guests_count'],
            apartment_class=row['apartment_class'],
            check_in=row['check_in'],
            check_out=row['check_out'],
            status=row['status'],
            notes=row['notes'] or '',
            created_at=row['created_at'],
        )

    def find_by_id(self, booking_id: int) -> Optional[Booking]:
        return self._map(super().find_by_id(booking_id))

    def find_all(self) -> List[Booking]:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM bookings ORDER BY created_at DESC')
            return [self._map(r) for r in cur.fetchall()]

    def find_by_client(self, client_id: int) -> List[Booking]:
        with db.cursor() as cur:
            cur.execute(
                'SELECT * FROM bookings WHERE client_id = %s ORDER BY created_at DESC',
                (client_id,),
            )
            return [self._map(r) for r in cur.fetchall()]

    def find_pending(self) -> List[Booking]:
        with db.cursor() as cur:
            cur.execute(
                "SELECT * FROM bookings WHERE status = 'pending' ORDER BY created_at",
            )
            return [self._map(r) for r in cur.fetchall()]

    def create(self, client_id: int, guests_count: int, apartment_class: str,
               check_in, check_out, notes: str = '') -> Booking:
        with db.cursor() as cur:
            cur.execute(
                '''INSERT INTO bookings
                       (client_id, guests_count, apartment_class, check_in, check_out, notes)
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING id''',
                (client_id, guests_count, apartment_class, check_in, check_out, notes),
            )
            booking_id = cur.fetchone()[0]
        logger.info("Created booking id=%s client=%s", booking_id, client_id)
        return self.find_by_id(booking_id)

    def approve(self, booking_id: int, room_id: int) -> Optional[Booking]:
        with db.cursor() as cur:
            cur.execute(
                "UPDATE bookings SET status = 'approved', room_id = %s WHERE id = %s",
                (room_id, booking_id),
            )
        logger.info("Approved booking id=%s room=%s", booking_id, room_id)
        return self.find_by_id(booking_id)

    def reject(self, booking_id: int) -> Optional[Booking]:
        with db.cursor() as cur:
            cur.execute(
                "UPDATE bookings SET status = 'rejected' WHERE id = %s",
                (booking_id,),
            )
        logger.info("Rejected booking id=%s", booking_id)
        return self.find_by_id(booking_id)
