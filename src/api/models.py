from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    VARCHAR, Column, String, Boolean,
    ForeignKey, Table,
)
from sqlalchemy.orm import (
    Mapped, DeclarativeBase,
    relationship, mapped_column,
)


class Base(DeclarativeBase):
    """
    This is magic that can be ignored
    for now!  It's a special tool
    that will help us later.   
    """


db = SQLAlchemy(model_class=Base)

# Association Table
user_to_collabpost = Table(
    "user_to_collabpost", Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("collab_post_id", ForeignKey("collab_posts.id")),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String(256), nullable=False,
    )

    posts: Mapped[List["Post"]] = relationship(
        back_populates="user", uselist=True
    )
    collab_posts: Mapped[List["CollabPost"]] = relationship(
        secondary=user_to_collabpost,
        back_populates="users",
        uselist=True,
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def serialize(self, include_rel=True):
        user_dict = {
            "id": self.id,
            "username": self.username,
        }

        if include_rel:
            return user_dict | {
                "posts": [post.serialize() for post in self.posts],
                "collab_posts": [post.serialize() for post in self.collab_posts],
            }

        return user_dict


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str] = mapped_column(VARCHAR)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="posts",
    )

    def __repr__(self):
        return f'<Post "{self.title}" by: {self.user.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.user.username,
        }


class CollabPost(Base):
    __tablename__ = "collab_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str] = mapped_column(VARCHAR)

    users: Mapped[List["User"]] = relationship(
        secondary=user_to_collabpost,
        back_populates="collab_posts",
        uselist=True,
    )

    def __repr__(self):
        return f'<Post "{self.title}">'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "users": [user.serialize(include_rel=False) for user in self.users]
        }
