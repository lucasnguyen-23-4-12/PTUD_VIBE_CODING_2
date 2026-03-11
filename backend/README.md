# Library Management System (MVP) — Backend

## Run (Windows / PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend API: `http://127.0.0.1:8000`  
Swagger UI: `http://127.0.0.1:8000/docs`

### Default account (auto-created on first run)

- username: `admin`
- password: `admin`
- role: `admin`

## Environment variables (optional)

- `DATABASE_URL` (default: `sqlite:///./library.db`)
- `SECRET_KEY` (default: `dev-secret-change-me`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default: `480`)

