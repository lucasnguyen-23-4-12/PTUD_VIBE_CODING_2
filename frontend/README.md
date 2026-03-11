# Library Management System (MVP) — Frontend

This is a simple static frontend (HTML + Bootstrap + Vanilla JS).

## Run

Option A (quick): open `frontend/login.html` in your browser.

Option B (recommended): serve it to avoid browser CORS/file restrictions:

```powershell
cd frontend
python -m http.server 5500
```

Then open: `http://127.0.0.1:5500/login.html`

## Backend API URL

Default is `http://127.0.0.1:8000`. If you change it, edit:

- `frontend/assets/api.js`

