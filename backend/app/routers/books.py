from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BookCopy, BookTitle
from ..schemas import (
    BookCopyCreate,
    BookCopyOut,
    BookCopyUpdate,
    BookTitleCreate,
    BookTitleOut,
    BookTitleUpdate,
)
from ..security import get_current_librarian


router = APIRouter(tags=["books"])


def _recalc_total_quantity(db: Session, title_id: int) -> None:
    total = db.scalar(select(func.count(BookCopy.copy_id)).where(BookCopy.title_id == title_id)) or 0
    title = db.get(BookTitle, title_id)
    if title:
        title.total_quantity = int(total)


# ----- Book Titles -----
@router.get("/titles", response_model=list[BookTitleOut])
def list_titles(db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return list(db.scalars(select(BookTitle).order_by(BookTitle.title_id)))


@router.get("/titles/{title_id}", response_model=BookTitleOut)
def get_title(title_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    title = db.get(BookTitle, title_id)
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    return title


@router.post("/titles", response_model=BookTitleOut)
def create_title(payload: BookTitleCreate, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    title = BookTitle(**payload.model_dump(), total_quantity=0)
    db.add(title)
    db.commit()
    db.refresh(title)
    return title


@router.put("/titles/{title_id}", response_model=BookTitleOut)
def update_title(
    title_id: int, payload: BookTitleUpdate, db: Session = Depends(get_db), _=Depends(get_current_librarian)
):
    title = db.get(BookTitle, title_id)
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(title, k, v)
    db.commit()
    db.refresh(title)
    return title


@router.delete("/titles/{title_id}")
def delete_title(title_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    title = db.get(BookTitle, title_id)
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    db.delete(title)
    db.commit()
    return {"ok": True}


# ----- Book Copies -----
@router.get("/copies", response_model=list[BookCopyOut])
def list_copies(db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return list(db.scalars(select(BookCopy).order_by(BookCopy.copy_id)))


@router.get("/copies/{copy_id}", response_model=BookCopyOut)
def get_copy(copy_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    copy = db.get(BookCopy, copy_id)
    if not copy:
        raise HTTPException(status_code=404, detail="Copy not found")
    return copy


@router.get("/titles/{title_id}/copies", response_model=list[BookCopyOut])
def list_copies_for_title(title_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return list(db.scalars(select(BookCopy).where(BookCopy.title_id == title_id).order_by(BookCopy.copy_id)))


@router.post("/copies", response_model=BookCopyOut)
def create_copy(payload: BookCopyCreate, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    title = db.get(BookTitle, payload.title_id)
    if not title:
        raise HTTPException(status_code=400, detail="Invalid title_id")
    copy = BookCopy(**payload.model_dump())
    db.add(copy)
    db.flush()
    _recalc_total_quantity(db, payload.title_id)
    db.commit()
    db.refresh(copy)
    return copy


@router.put("/copies/{copy_id}", response_model=BookCopyOut)
def update_copy(
    copy_id: int, payload: BookCopyUpdate, db: Session = Depends(get_db), _=Depends(get_current_librarian)
):
    copy = db.get(BookCopy, copy_id)
    if not copy:
        raise HTTPException(status_code=404, detail="Copy not found")
    data = payload.model_dump(exclude_unset=True)
    old_title_id = copy.title_id
    for k, v in data.items():
        setattr(copy, k, v)
    db.flush()
    _recalc_total_quantity(db, old_title_id)
    _recalc_total_quantity(db, copy.title_id)
    db.commit()
    db.refresh(copy)
    return copy


@router.delete("/copies/{copy_id}")
def delete_copy(copy_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    copy = db.get(BookCopy, copy_id)
    if not copy:
        raise HTTPException(status_code=404, detail="Copy not found")
    title_id = copy.title_id
    db.delete(copy)
    db.flush()
    _recalc_total_quantity(db, title_id)
    db.commit()
    return {"ok": True}
