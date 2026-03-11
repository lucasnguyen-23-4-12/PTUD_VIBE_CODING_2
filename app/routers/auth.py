from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Librarian
from ..schemas import LoginIn, TokenOut
from ..security import create_access_token, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    librarian = db.scalar(select(Librarian).where(Librarian.username == payload.username))
    if not librarian or not verify_password(payload.password, librarian.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username/password")

    token = create_access_token(subject=str(librarian.librarian_id), role=librarian.role)
    return {"access_token": token, "token_type": "bearer", "librarian": librarian}

