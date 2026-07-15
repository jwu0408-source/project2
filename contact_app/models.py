from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    categories: Mapped[list["Category"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    contacts: Mapped[list["Contact"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    login_sessions: Mapped[list["LoginSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class LoginSession(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    user: Mapped[User] = relationship(back_populates="login_sessions")


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_category_user_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    user: Mapped[User] = relationship(back_populates="categories")
    contacts: Mapped[list["Contact"]] = relationship(back_populates="category", cascade="all, delete-orphan")


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (UniqueConstraint("user_id", "phone", name="uq_contact_user_phone"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    addr: Mapped[str] = mapped_column(String(100), nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)

    user: Mapped[User] = relationship(back_populates="contacts")
    category: Mapped[Category | None] = relationship(back_populates="contacts")
