import hashlib
import logging
from typing import Optional

from app.core.database import db
from app.dao.base_dao import BaseDAO
from app.models.user import User

logger = logging.getLogger(__name__)


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class UserDAO(BaseDAO):
    table = 'users'

    def _map(self, row) -> Optional[User]:
        if row is None:
            return None
        return User(
            id=row['id'],
            username=row['username'],
            password_hash=row['password_hash'],
            role=row['role'],
            full_name=row['full_name'],
            email=row['email'],
            created_at=row['created_at'],
        )

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._map(super().find_by_id(user_id))

    def find_by_username(self, username: str) -> Optional[User]:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE username = %s', (username,))
            return self._map(cur.fetchone())

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.find_by_username(username)
        if user and user.password_hash == _hash(password):
            logger.info("Authenticated user: %s", username)
            return user
        logger.warning("Failed authentication: %s", username)
        return None

    def create(self, username: str, password: str, role: str,
               full_name: str, email: str) -> User:
        with db.cursor() as cur:
            cur.execute(
                '''INSERT INTO users (username, password_hash, role, full_name, email)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id''',
                (username, _hash(password), role, full_name, email),
            )
            user_id = cur.fetchone()[0]
        logger.info("Created user id=%s role=%s", user_id, role)
        return self.find_by_id(user_id)
