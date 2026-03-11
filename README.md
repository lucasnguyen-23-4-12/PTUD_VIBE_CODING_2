# University Library Management System (MVP)

FastAPI + SQLite + SQLAlchemy backend, with a simple Bootstrap + Vanilla JS frontend.

## Run backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Default admin account is auto-created on first run:

- username: `admin`
- password: `admin`

## Run frontend

```powershell
cd frontend
python -m http.server 5500
```

Open: `http://127.0.0.1:5500/login.html`

## Notes

- API docs: `http://127.0.0.1:8000/docs`
- Database file (default): `backend/library.db`

