from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class MajorBase(BaseModel):
    major_name: str
    description: str | None = None


class MajorCreate(MajorBase):
    pass


class MajorUpdate(BaseModel):
    major_name: str | None = None
    description: str | None = None


class MajorOut(MajorBase):
    model_config = ConfigDict(from_attributes=True)
    major_id: int


class ReaderBase(BaseModel):
    name: str
    class_: str = Field(alias="class")
    birth_date: date
    gender: str

    model_config = ConfigDict(populate_by_name=True)


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(BaseModel):
    name: str | None = None
    class_: str | None = Field(default=None, alias="class")
    birth_date: date | None = None
    gender: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class ReaderOut(ReaderBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    reader_id: int


class BookTitleBase(BaseModel):
    title_name: str
    publisher: str
    pages: int
    size: str
    author: str
    major_id: int


class BookTitleCreate(BookTitleBase):
    pass


class BookTitleUpdate(BaseModel):
    title_name: str | None = None
    publisher: str | None = None
    pages: int | None = None
    size: str | None = None
    author: str | None = None
    major_id: int | None = None


class BookTitleOut(BookTitleBase):
    model_config = ConfigDict(from_attributes=True)
    title_id: int
    total_quantity: int


class BookCopyBase(BaseModel):
    title_id: int
    status: str = "available"
    import_date: date


class BookCopyCreate(BookCopyBase):
    pass


class BookCopyUpdate(BaseModel):
    status: str | None = None
    import_date: date | None = None
    title_id: int | None = None


class BookCopyOut(BookCopyBase):
    model_config = ConfigDict(from_attributes=True)
    copy_id: int


class LibrarianBase(BaseModel):
    name: str
    username: str
    role: str = "librarian"


class LibrarianCreate(LibrarianBase):
    password: str


class LibrarianUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    role: str | None = None
    password: str | None = None


class LibrarianOut(LibrarianBase):
    model_config = ConfigDict(from_attributes=True)
    librarian_id: int


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    librarian: LibrarianOut


class BorrowCreate(BaseModel):
    reader_id: int
    copy_id: int


class BorrowOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    borrow_id: int
    copy_id: int
    reader_id: int
    librarian_id: int
    borrow_date: datetime
    status: str


class ReturnIn(BaseModel):
    borrow_id: int


class MostBorrowedRow(BaseModel):
    title_id: int
    title_name: str
    borrow_count: int


class UnreturnedReaderRow(BaseModel):
    reader_id: int
    name: str
    class_name: str = Field(alias="class")
    borrow_id: int
    copy_id: int
    title_id: int
    title_name: str
    borrow_date: datetime

    model_config = ConfigDict(populate_by_name=True)
