# PMSSS Scholarship Portal (Django + MySQL)

A minimal full‑stack portal with modules for Students, Institutes, SAG, and Finance Bureau. Includes Django admin, basic templates, and REST CRUD APIs.

## Features
- Django + DRF APIs under `/api/`
- Apps: students, institutes, sag, finance
- Institute has `admission_status` and `esuvidha_status`
- Basic CRUD UI (list/create/edit/delete)
- MySQL-ready via `.env` (fallback to SQLite for first run)

## Setup (Windows, cmd.exe)

1. Create and activate virtualenv (if not already):
```
python -m venv .venv
".venv\Scripts\activate"
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create `.env` from example and adjust values (MySQL credentials):
```
copy .env.example .env
```

4. Initialize project (first time only, if code not already generated):
```
python -m django --version
python -m django startproject pmsss_portal .
```

5. Apply migrations and create superuser:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. Run the server:
```
python manage.py runserver
```

Visit http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/.

## Environment
- Django 5.x
- DRF 3.15
- MySQL via PyMySQL (or SQLite by default)

## Notes
- If MySQL is not installed, the project will use SQLite automatically.
- Update `ALLOWED_HOSTS` if accessing from another device.
"# PMSSS" 
