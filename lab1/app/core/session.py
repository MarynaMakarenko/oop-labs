import logging
import time
import uuid
from http.cookies import SimpleCookie
from typing import Optional

import config

logger = logging.getLogger(__name__)


class Session:
    """In-memory session object identified by a UUID stored in a cookie."""

    def __init__(self, session_id: str, expires_at: float):
        self.id = session_id
        self.expires_at = expires_at
        self._data: dict = {}

    def is_valid(self) -> bool:
        return time.time() < self.expires_at

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value

    def remove(self, key: str) -> None:
        self._data.pop(key, None)


class SessionManager:
    """
    Manages server-side sessions.

    Each session is identified by a UUID stored in an HTTP-only cookie.
    Sessions are kept in memory and expire after SESSION_EXPIRE_SECONDS.
    """

    def __init__(self):
        self._store: dict[str, Session] = {}

    def create(self) -> Session:
        sid = str(uuid.uuid4())
        session = Session(sid, time.time() + config.SESSION_EXPIRE_SECONDS)
        self._store[sid] = session
        logger.debug("Session created: %s", sid)
        return session

    def get(self, session_id: str) -> Optional[Session]:
        session = self._store.get(session_id)
        if session is None:
            return None
        if not session.is_valid():
            del self._store[session_id]
            logger.debug("Session expired: %s", session_id)
            return None
        return session

    def destroy(self, session_id: str) -> None:
        self._store.pop(session_id, None)
        logger.debug("Session destroyed: %s", session_id)

    def from_request(self, headers) -> Optional[Session]:
        raw = headers.get('Cookie', '')
        if not raw:
            return None
        cookies = SimpleCookie()
        cookies.load(raw)
        morsel = cookies.get(config.SESSION_COOKIE_NAME)
        return self.get(morsel.value) if morsel else None

    @staticmethod
    def set_cookie(session_id: str) -> str:
        c = SimpleCookie()
        c[config.SESSION_COOKIE_NAME] = session_id
        c[config.SESSION_COOKIE_NAME]['path'] = '/'
        c[config.SESSION_COOKIE_NAME]['max-age'] = config.SESSION_EXPIRE_SECONDS
        c[config.SESSION_COOKIE_NAME]['httponly'] = True
        return c.output(header='').strip()

    @staticmethod
    def clear_cookie() -> str:
        c = SimpleCookie()
        c[config.SESSION_COOKIE_NAME] = ''
        c[config.SESSION_COOKIE_NAME]['path'] = '/'
        c[config.SESSION_COOKIE_NAME]['max-age'] = 0
        return c.output(header='').strip()


sessions = SessionManager()
