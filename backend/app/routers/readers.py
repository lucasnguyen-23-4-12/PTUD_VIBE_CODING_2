from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Reader
from ..schemas import ReaderCreate, ReaderOut, ReaderUpdate
from ..security import get_current_librarian


router = APIRouter(prefix="/readers", tags=["readers"])


@router.get("", response_model=list[ReaderOut])
def list_readers(db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return list(db.scalars(select(Reader).order_by(Reader.reader_id)))


@router.get("/{reader_id}", response_model=ReaderOut)
def get_reader(reader_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    reader = db.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader


@router.post("", response_model=ReaderOut)
def create_reader(payload: ReaderCreate, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    reader = Reader(
        name=payload.name,
        class_=payload.class_,
        birth_date=payload.birth_date,
        gender=payload.gender,
    )
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


@router.put("/{reader_id}", response_model=ReaderOut)
def update_reader(
    reader_id: int, payload: ReaderUpdate, db: Session = Depends(get_db), _=Depends(get_current_librarian)
):
    reader = db.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    if "class_" in data:
        reader.class_ = data.pop("class_")
    for k, v in data.items():
        setattr(reader, k, v)
    db.commit()
    db.refresh(reader)
    return reader


@router.delete("/{reader_id}")
def delete_reader(reader_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    reader = db.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    db.delete(reader)
    db.commit()
    return {"ok": True}
