import logging
from typing import List, Optional

from app.core.database import db
from app.dao.base_dao import BaseDAO
from app.models.invoice import Invoice

logger = logging.getLogger(__name__)


class InvoiceDAO(BaseDAO):
    table = 'invoices'

    def _map(self, row) -> Optional[Invoice]:
        if row is None:
            return None
        return Invoice(
            id=row['id'],
            booking_id=row['booking_id'],
            amount=float(row['amount']),
            status=row['status'],
            issued_at=row['issued_at'],
            paid_at=row['paid_at'],
        )

    def find_by_id(self, invoice_id: int) -> Optional[Invoice]:
        return self._map(super().find_by_id(invoice_id))

    def find_all(self) -> List[Invoice]:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM invoices ORDER BY issued_at DESC')
            return [self._map(r) for r in cur.fetchall()]

    def find_by_booking(self, booking_id: int) -> Optional[Invoice]:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM invoices WHERE booking_id = %s', (booking_id,))
            return self._map(cur.fetchone())

    def find_by_client(self, client_id: int) -> List[Invoice]:
        with db.cursor() as cur:
            cur.execute(
                '''SELECT i.* FROM invoices i
                   JOIN bookings b ON b.id = i.booking_id
                   WHERE b.client_id = %s
                   ORDER BY i.issued_at DESC''',
                (client_id,),
            )
            return [self._map(r) for r in cur.fetchall()]

    def create(self, booking_id: int, amount: float) -> Invoice:
        with db.cursor() as cur:
            cur.execute(
                'INSERT INTO invoices (booking_id, amount) VALUES (%s, %s) RETURNING id',
                (booking_id, amount),
            )
            invoice_id = cur.fetchone()[0]
        logger.info("Created invoice id=%s booking=%s amount=%.2f", invoice_id, booking_id, amount)
        return self.find_by_id(invoice_id)

    def mark_paid(self, invoice_id: int) -> Optional[Invoice]:
        with db.cursor() as cur:
            cur.execute(
                "UPDATE invoices SET status = 'paid', paid_at = NOW() WHERE id = %s",
                (invoice_id,),
            )
        logger.info("Invoice %s marked paid", invoice_id)
        return self.find_by_id(invoice_id)
