import uuid
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .security import hash_password, verify_password


def create_user(db: Session, payload: schemas.SignupIn) -> models.User:
    existing = db.scalar(select(models.User).where(models.User.username == payload.username))
    if existing:
        raise HTTPException(status_code=409, detail="duplicate username")

    user = models.User(username=payload.username, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    default_categories = ["가족", "친구", "기타"]
    for name in default_categories:
        db.add(models.Category(user_id=user.id, name=name))
    db.commit()
    return user


def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    user = db.scalar(select(models.User).where(models.User.username == username))
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_login_session(db: Session, user_id: int) -> str:
    token = str(uuid.uuid4())
    session = models.LoginSession(user_id=user_id, token=token)
    db.add(session)
    db.commit()
    return token


def delete_login_session(db: Session, token: str) -> None:
    session = db.scalar(select(models.LoginSession).where(models.LoginSession.token == token))
    if session:
        db.delete(session)
        db.commit()


def get_user_by_token(db: Session, token: str) -> models.User | None:
    session = db.scalar(select(models.LoginSession).where(models.LoginSession.token == token))
    if not session:
        return None
    return session.user


def list_categories(db: Session, user_id: int) -> list[models.Category]:
    return db.scalars(
        select(models.Category)
        .where(models.Category.user_id == user_id)
        .order_by(models.Category.id)
    ).all()


def create_category(db: Session, user_id: int, payload: schemas.CategoryCreate) -> models.Category:
    existing = db.scalar(select(models.Category).where(models.Category.user_id == user_id, models.Category.name == payload.name))
    if existing:
        raise HTTPException(status_code=409, detail="duplicate category name")

    category = models.Category(user_id=user_id, name=payload.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, user_id: int, payload: schemas.CategoryCreate) -> models.Category:
    category = db.get(models.Category, category_id)
    if not category or category.user_id != user_id:
        raise HTTPException(status_code=404, detail="category not found")
    if category.name != payload.name:
        existing = db.scalar(select(models.Category).where(models.Category.user_id == user_id, models.Category.name == payload.name))
        if existing:
            raise HTTPException(status_code=409, detail="duplicate category name")
    category.name = payload.name
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int, user_id: int) -> None:
    category = db.get(models.Category, category_id)
    if not category or category.user_id != user_id:
        raise HTTPException(status_code=404, detail="category not found")
    if category.contacts:
        raise HTTPException(status_code=409, detail="category is in use")
    db.delete(category)
    db.commit()


def count_contacts_in_category(db: Session, category_id: int) -> int:
    return db.scalar(select(models.Contact).where(models.Contact.category_id == category_id).count())


def list_contacts(db: Session, user_id: int, name: str | None = None) -> list[models.Contact]:
    query = select(models.Contact).where(models.Contact.user_id == user_id)
    if name:
        query = query.where(models.Contact.name.contains(name))
    return db.scalars(query).all()


def create_contact(db: Session, user_id: int, payload: schemas.ContactCreate) -> models.Contact:
    existing = db.scalar(select(models.Contact).where(models.Contact.user_id == user_id, models.Contact.phone == payload.phone))
    if existing:
        raise HTTPException(status_code=409, detail="duplicate phone number")

    contact = models.Contact(
        user_id=user_id,
        name=payload.name,
        phone=payload.phone,
        addr=payload.addr,
        category_id=payload.category_id,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_my_contact(db: Session, contact_id: int, user_id: int) -> models.Contact:
    contact = db.get(models.Contact, contact_id)
    if not contact or contact.user_id != user_id:
        raise HTTPException(status_code=404, detail="contact not found")
    return contact


def update_contact(db: Session, contact_id: int, user_id: int, payload: schemas.ContactUpdate) -> models.Contact:
    contact = db.get(models.Contact, contact_id)
    if not contact or contact.user_id != user_id:
        raise HTTPException(status_code=404, detail="contact not found")

    if payload.phone and payload.phone != contact.phone:
        existing = db.scalar(select(models.Contact).where(models.Contact.user_id == user_id, models.Contact.phone == payload.phone))
        if existing:
            raise HTTPException(status_code=409, detail="duplicate phone number")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: int, user_id: int) -> None:
    contact = db.get(models.Contact, contact_id)
    if not contact or contact.user_id != user_id:
        raise HTTPException(status_code=404, detail="contact not found")
    db.delete(contact)
    db.commit()
