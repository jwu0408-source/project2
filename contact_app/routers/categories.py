from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[schemas.CategoryOut])
def list_categories(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.list_categories(db, user.id)


@router.post("", status_code=201, response_model=schemas.CategoryOut)
def create_category(payload: schemas.CategoryCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_category(db, user.id, payload)


@router.patch("/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, payload: schemas.CategoryCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_category(db, category_id, user.id, payload)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_category(db, category_id, user.id)
    return Response(status_code=204)
