from pydantic import BaseModel

from src.database.database import SessionFactory
from src.database.model import DatabaseUser


class UserRepository(BaseModel):
    session_factory: SessionFactory
    def ensure_exists(self, user_email: str, user_name: str) -> None:
        with self.session_factory() as session:
            result = session.query(DatabaseUser) \
                .filter((DatabaseUser.email == user_email)) \
                .first()
            if result is None:
                user = DatabaseUser(
                    email=user_email,
                    name=user_name
                )
                session.add(user)
                session.commit()