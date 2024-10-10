from app import db
from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, String, DateTime, ForeignKey
from typing import List


def generate_uuid() -> str:
    return str(uuid4())


class User(db.Model):
    __tablename__ = 'users'

    uuid: Mapped[str] = mapped_column(primary_key=True, unique=True, default=generate_uuid)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[str] = mapped_column(DateTime(), server_default=func.now())

    posts: Mapped[List['Post']] = relationship(cascade='all, delete-orphan')


class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    preview: Mapped[str] = mapped_column(String(260))
    title: Mapped[str] = mapped_column(String(120), index=True)
    content: Mapped[str]
    reading_time: Mapped[int]
    author_id: Mapped[str] = mapped_column(ForeignKey('users.uuid'))
    created_at: Mapped[str] = mapped_column(DateTime(), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(), nullable=True, onupdate=func.now())

    tags: Mapped[List['PostTag']] = relationship(cascade='all, delete-orphan')
    author: Mapped[List['User']] = relationship(viewonly=True)


class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'), primary_key=True)

    post: Mapped[List['Post']] = relationship(viewonly=True)
    tag: Mapped[List['Tag']] = relationship(viewonly=True)


class Tag(db.Model):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
