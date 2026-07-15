from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("", response_model=list[schemas.ContactOut])
def list_contacts(name: str | None = None, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.list_contacts(db, user.id, name=name)


@router.post("", status_code=201, response_model=schemas.ContactOut)
def create_contact(payload: schemas.ContactCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_contact(db, user.id, payload)


@router.get("/{contact_id}", response_model=schemas.ContactOut)
def get_contact(contact_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_my_contact(db, contact_id, user.id)


@router.patch("/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, payload: schemas.ContactUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_contact(db, contact_id, user.id, payload)


@router.delete("/{contact_id}", status_code=204)
def delete_contact(contact_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_contact(db, contact_id, user.id)
    return Response(status_code=204)
