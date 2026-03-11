from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BookCopy, BookTitle, BorrowRecord, Reader
from ..schemas import MostBorrowedRow, UnreturnedReaderRow
from ..security import get_current_librarian


router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/most-borrowed", response_model=list[MostBorrowedRow])
def most_borrowed(db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    stmt = (
        select(BookTitle.title_id, BookTitle.title_name, func.count(BorrowRecord.borrow_id).label("borrow_count"))
        .select_from(BorrowRecord)
        .join(BookCopy, BookCopy.copy_id == BorrowRecord.copy_id)
        .join(BookTitle, BookTitle.title_id == BookCopy.title_id)
        .group_by(BookTitle.title_id, BookTitle.title_name)
        .order_by(func.count(BorrowRecord.borrow_id).desc())
        .limit(20)
    )
    rows = db.execute(stmt).all()
    return [{"title_id": r.title_id, "title_name": r.title_name, "borrow_count": int(r.borrow_count)} for r in rows]


@router.get("/unreturned-readers", response_model=list[UnreturnedReaderRow])
def unreturned_readers(db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    stmt = (
        select(
            Reader.reader_id,
            Reader.name,
            Reader.class_.label("class"),
            BorrowRecord.borrow_id,
            BorrowRecord.copy_id,
            BookTitle.title_id,
            BookTitle.title_name,
            BorrowRecord.borrow_date,
        )
        .select_from(BorrowRecord)
        .join(Reader, Reader.reader_id == BorrowRecord.reader_id)
        .join(BookCopy, BookCopy.copy_id == BorrowRecord.copy_id)
        .join(BookTitle, BookTitle.title_id == BookCopy.title_id)
        .where(BorrowRecord.status == "borrowed")
        .order_by(BorrowRecord.borrow_date.asc())
    )
    rows = db.execute(stmt).mappings().all()
    return [dict(r) for r in rows]
