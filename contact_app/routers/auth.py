from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
SESSION_COOKIE_NAME = "session_id"


def get_current_user(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_id:
        raise HTTPException(status_code=401, detail="missing token")
    user = crud.get_user_by_token(db, session_id)
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")
    return user


@router.post("/signup", status_code=201, response_model=schemas.UserOut)
def signup(payload: schemas.SignupIn, db: Session = Depends(get_db)):
    user = crud.create_user(db, payload)
    return user


@router.post("/login", response_model=schemas.TokenOut)
def login(payload: schemas.SignupIn, response: Response, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = crud.create_login_session(db, user.id)
    response.set_cookie(key=SESSION_COOKIE_NAME, value=token, httponly=True, samesite="lax")
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id:
        crud.delete_login_session(db, session_id)
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return {"detail": "logged out"}


@router.get("/me", response_model=schemas.UserOut)
def get_me(user=Depends(get_current_user)):
    return user
