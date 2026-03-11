from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BookCopy, BorrowRecord, Reader
from ..schemas import BorrowCreate, BorrowOut, ReturnIn
from ..security import get_current_librarian


router = APIRouter(prefix="/borrows", tags=["borrows"])


@router.get("", response_model=list[BorrowOut])
def list_borrows(db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return list(db.scalars(select(BorrowRecord).order_by(BorrowRecord.borrow_id.desc())))


@router.post("/borrow", response_model=BorrowOut)
def borrow_book(
    payload: BorrowCreate,
    db: Session = Depends(get_db),
    current=Depends(get_current_librarian),
):
    reader = db.get(Reader, payload.reader_id)
    if not reader:
        raise HTTPException(status_code=400, detail="Invalid reader_id")

    active_borrow = db.scalar(
        select(BorrowRecord).where(BorrowRecord.reader_id == payload.reader_id, BorrowRecord.status == "borrowed")
    )
    if active_borrow:
        raise HTTPException(status_code=400, detail="Reader already has an active borrowed book")

    copy = db.get(BookCopy, payload.copy_id)
    if not copy:
        raise HTTPException(status_code=400, detail="Invalid copy_id")
    if copy.status != "available":
        raise HTTPException(status_code=400, detail="Copy is not available")

    copy.status = "borrowed"
    borrow = BorrowRecord(
        copy_id=copy.copy_id,
        reader_id=payload.reader_id,
        librarian_id=current.librarian_id,
        borrow_date=datetime.now(timezone.utc),
        status="borrowed",
    )
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


@router.post("/return", response_model=BorrowOut)
def return_book(
    payload: ReturnIn,
    db: Session = Depends(get_db),
    _=Depends(get_current_librarian),
):
    borrow = db.get(BorrowRecord, payload.borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow.status != "borrowed":
        raise HTTPException(status_code=400, detail="Borrow record already returned")

    copy = db.get(BookCopy, borrow.copy_id)
    if copy:
        copy.status = "available"
    borrow.status = "returned"
    db.commit()
    db.refresh(borrow)
    return borrow

