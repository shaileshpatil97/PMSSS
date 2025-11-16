# PMSSS Scholarship Portal (Django)

An original, clean, PMSSS-inspired scholarship portal with modules for Students, Institutes, SAG, Finance, and Scholarships. Includes Django admin, modern Bootstrap UI, and REST-ready APIs.

## Features
- Modern Bootstrap 5 UI and shared layout
- Apps: students, institutes, sag, finance, scholarships
- Application lifecycle views with filters and status badges
- DRF installed; API routes mounted at `/api/`
- MySQL-ready via `.env` (falls back to SQLite)

## Run locally (Windows cmd.exe)

Optional: create and activate a venv first.

```
python -m venv .venv
".venv\Scripts\activate"
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/.

## Roadmap (PMSSS-like)
- Student/citizen login and profile
- Role dashboards: Institute, Department, Finance
- OTP login and notifications (email/SMS)
- Application audit trail and document checklist
- Payment initiation and disbursement ledger
- Reports/export (CSV/XLSX)

## Notes
- Update `ALLOWED_HOSTS` in production; set `DEBUG=False` and a strong `SECRET_KEY` in `.env`.
- Static files are served via Django for dev; use `collectstatic` behind a web server in production.
