from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Librarian
from ..schemas import LibrarianCreate, LibrarianOut, LibrarianUpdate
from ..security import hash_password, require_admin


router = APIRouter(prefix="/librarians", tags=["librarians"])


@router.get("", response_model=list[LibrarianOut])
def list_librarians(db: Session = Depends(get_db), _=Depends(require_admin)):
    return list(db.scalars(select(Librarian).order_by(Librarian.librarian_id)))


@router.post("", response_model=LibrarianOut)
def create_librarian(payload: LibrarianCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    librarian = Librarian(
        name=payload.name,
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(librarian)
    db.commit()
    db.refresh(librarian)
    return librarian


@router.put("/{librarian_id}", response_model=LibrarianOut)
def update_librarian(
    librarian_id: int, payload: LibrarianUpdate, db: Session = Depends(get_db), _=Depends(require_admin)
):
    librarian = db.get(Librarian, librarian_id)
    if not librarian:
        raise HTTPException(status_code=404, detail="Librarian not found")

    data = payload.model_dump(exclude_unset=True)
    if "password" in data:
        librarian.password_hash = hash_password(data.pop("password"))
    for k, v in data.items():
        setattr(librarian, k, v)
    db.commit()
    db.refresh(librarian)
    return librarian


@router.delete("/{librarian_id}")
def delete_librarian(librarian_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    librarian = db.get(Librarian, librarian_id)
    if not librarian:
        raise HTTPException(status_code=404, detail="Librarian not found")
    db.delete(librarian)
    db.commit()
    return {"ok": True}

