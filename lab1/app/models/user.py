from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Domain model for a system user (client or admin)."""

    id: Optional[int]
    username: str
    password_hash: str
    role: str          # 'client' | 'admin'
    full_name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def is_client(self) -> bool:
        return self.role == 'client'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'full_name': self.full_name,
            'email': self.email,
        }
