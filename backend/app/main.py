from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from .database import SessionLocal, engine
from .models import Base, Librarian
from .routers import auth, books, borrows, librarians, majors, readers, reports
from .security import hash_password


def create_app() -> FastAPI:
    app = FastAPI(title="University Library Management System (MVP)")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(readers.router)
    app.include_router(majors.router)
    app.include_router(books.router)
    app.include_router(borrows.router)
    app.include_router(reports.router)
    app.include_router(librarians.router)

    @app.get("/")
    def root():
        return {"name": "library-mvp", "docs": "/docs"}

    return app


app = create_app()


def _init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.scalar(select(Librarian).limit(1))
        if not existing:
            admin = Librarian(
                name="System Admin",
                username="admin",
                password_hash=hash_password("admin"),
                role="admin",
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


_init_db()

