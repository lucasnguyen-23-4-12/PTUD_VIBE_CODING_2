from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Major(Base):
    __tablename__ = "majors"

    major_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    major_name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    titles: Mapped[list["BookTitle"]] = relationship(back_populates="major")


class Reader(Base):
    __tablename__ = "readers"

    reader_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    class_: Mapped[str] = mapped_column("class", String(100), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)

    borrows: Mapped[list["BorrowRecord"]] = relationship(back_populates="reader")


class BookTitle(Base):
    __tablename__ = "book_titles"

    title_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title_name: Mapped[str] = mapped_column(String(250), nullable=False)
    publisher: Mapped[str] = mapped_column(String(200), nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    size: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(200), nullable=False)
    total_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    major_id: Mapped[int] = mapped_column(ForeignKey("majors.major_id", ondelete="RESTRICT"), nullable=False)

    major: Mapped["Major"] = relationship(back_populates="titles")
    copies: Mapped[list["BookCopy"]] = relationship(back_populates="title", cascade="all, delete-orphan")


class BookCopy(Base):
    __tablename__ = "book_copies"

    copy_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title_id: Mapped[int] = mapped_column(ForeignKey("book_titles.title_id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="available")  # available|borrowed
    import_date: Mapped[date] = mapped_column(Date, nullable=False)

    title: Mapped["BookTitle"] = relationship(back_populates="copies")
    borrows: Mapped[list["BorrowRecord"]] = relationship(back_populates="copy")


class Librarian(Base):
    __tablename__ = "librarians"
    __table_args__ = (UniqueConstraint("username", name="uq_librarians_username"),)

    librarian_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="librarian")  # admin|librarian

    borrows: Mapped[list["BorrowRecord"]] = relationship(back_populates="librarian")


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    borrow_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    copy_id: Mapped[int] = mapped_column(ForeignKey("book_copies.copy_id", ondelete="RESTRICT"), nullable=False)
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.reader_id", ondelete="RESTRICT"), nullable=False)
    librarian_id: Mapped[int] = mapped_column(ForeignKey("librarians.librarian_id", ondelete="RESTRICT"), nullable=False)
    borrow_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="borrowed")  # borrowed|returned

    copy: Mapped["BookCopy"] = relationship(back_populates="borrows")
    reader: Mapped["Reader"] = relationship(back_populates="borrows")
    librarian: Mapped["Librarian"] = relationship(back_populates="borrows")

