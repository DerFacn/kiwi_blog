from app import db
from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, String, DateTime


def generate_uuid() -> str:
    return str(uuid4())


class User(db.Model):
    __tablename__ = 'users'

    uuid: Mapped[str] = mapped_column(primary_key=True, unique=True, default=generate_uuid)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[str] = mapped_column(DateTime(), server_default=func.now())
