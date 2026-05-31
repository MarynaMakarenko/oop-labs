import logging
from typing import List, Optional

from app.core.database import db

logger = logging.getLogger(__name__)


class BaseDAO:
    """
    Abstract base Data Access Object.

    Provides generic CRUD skeletons so concrete DAOs only need
    to implement model-specific logic.
    """

    table: str = ''

    def find_by_id(self, entity_id: int):
        with db.cursor() as cur:
            cur.execute(f'SELECT * FROM {self.table} WHERE id = %s', (entity_id,))
            return cur.fetchone()

    def find_all(self):
        with db.cursor() as cur:
            cur.execute(f'SELECT * FROM {self.table} ORDER BY id')
            return cur.fetchall()

    def delete(self, entity_id: int) -> None:
        with db.cursor() as cur:
            cur.execute(f'DELETE FROM {self.table} WHERE id = %s', (entity_id,))
        logger.info("Deleted %s id=%s", self.table, entity_id)
