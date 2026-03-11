from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Major
from ..schemas import MajorCreate, MajorOut, MajorUpdate
from ..security import get_current_librarian


router = APIRouter(prefix="/majors", tags=["majors"])


@router.get("", response_model=list[MajorOut])
def list_majors(db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return list(db.scalars(select(Major).order_by(Major.major_id)))


@router.post("", response_model=MajorOut)
def create_major(payload: MajorCreate, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    major = Major(**payload.model_dump())
    db.add(major)
    db.commit()
    db.refresh(major)
    return major


@router.put("/{major_id}", response_model=MajorOut)
def update_major(major_id: int, payload: MajorUpdate, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    major = db.get(Major, major_id)
    if not major:
        raise HTTPException(status_code=404, detail="Major not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(major, k, v)
    db.commit()
    db.refresh(major)
    return major


@router.delete("/{major_id}")
def delete_major(major_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    major = db.get(Major, major_id)
    if not major:
        raise HTTPException(status_code=404, detail="Major not found")
    db.delete(major)
    db.commit()
    return {"ok": True}

