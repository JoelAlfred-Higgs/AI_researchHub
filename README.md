# AI Research Hub

A backend API for organizing research notes into categories, with user authentication and resource-level access control.

## Features

- User registration and login
- JWT-based authentication
- Create, retrieve, update, and delete research notes
- Organize notes into categories
- Restrict access to resources by user ownership
- Request validation and structured HTTP error responses
- MySQL persistence using SQLAlchemy
- Database schema migrations with Alembic
- Interactive API documentation with Swagger UI

## Tech Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT bearer tokens
- **Password Security:** `pwdlib`
- **Migrations:** Alembic
- **Testing:** pytest

## Project Structure

- `main.py` — application entry point
- `routers/` — user, notes, and category endpoints
- `crud.py` — database operations
- `models.py` — SQLAlchemy models
- `schemas.py` — request and response validation
- `DataBase.py` — database connection and session management
- `security.py` — password hashing and JWT creation
- `dependencies.py` — authentication dependencies
- `migrations/` — Alembic migration files
- `test/` — automated tests
- `.env` — local environment configuration (not committed)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/JoelAlfred-Higgs/AI_researchHub.git
cd AI_researchHub
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file with your local MySQL connection settings and JWT configuration. Use your own credentials and a securely generated JWT secret. Never commit `.env`.

### 5. Apply database migrations

```bash
python -m alembic -c App/alembic.ini upgrade head
```

### 6. Start the API

```bash
uvicorn App.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

## Run Tests

```bash
python -m pytest -v
```

## Current Status

The API includes authentication, user-specific notes and categories, and database migrations. Automated tests and endpoint behavior should be verified as the project evolves.

## Future Improvements

- Search and filter research notes
- Pagination for large collections
- Note tags and metadata
- Automated integration tests for notes and categories
- Deployment and CI/CD
