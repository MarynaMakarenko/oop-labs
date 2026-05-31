import logging
from contextlib import contextmanager

import psycopg2
import psycopg2.extras

import config

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Singleton that manages a single psycopg2 connection."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = None
        return cls._instance

    def get_connection(self):
        if self._conn is None or self._conn.closed:
            logger.info("Opening database connection")
            self._conn = psycopg2.connect(**config.DB_CONFIG)
        return self._conn

    @contextmanager
    def cursor(self):
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()
            logger.info("Database connection closed")


db = DatabaseConnection()
