# 📝 Notes Backend API

A production-style REST API built with **FastAPI** featuring JWT authentication, per-user notes with ownership enforcement, and a clean layered architecture.

---

## Features

- 🔐 **JWT Authentication** — register, login, and protected routes
- 📝 **Per-user Notes** — full CRUD with strict ownership enforcement
- 🗄️ **SQLAlchemy ORM** — clean database layer with SQLite
- 🔄 **Alembic Migrations** — safe schema changes without data loss
- ✅ **Pydantic v2 Validation** — strict request/response schemas
- 🛡️ **Password Hashing** — bcrypt via passlib, never plain text
- 📊 **Request Logging** — method, URL, status, duration on every request
- ⚠️ **Global Error Handling** — structured JSON errors across the entire API

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | SQLite via SQLAlchemy |
| Migrations | Alembic |
| Auth | JWT via python-jose |
| Password Hashing | bcrypt via passlib |
| Validation | Pydantic v2 |
| Server | Uvicorn |

---

## Project Structure

```
notes-backend/
├── main.py              # App setup, middleware, exception handlers, router registration
├── database.py          # Engine, SessionLocal, Base
├── db_model.py          # SQLAlchemy table models (UserDB, NotesDB)
├── models.py            # Pydantic schemas (request/response shapes)
├── routers/
│   ├── user.py          # Auth routes — register, login, get_current_user
│   └── notes.py         # Notes routes — CRUD, ownership enforced
└── alembic/
    └── versions/        # Migration history
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/divyakarn/notes-backend-.git
cd notes-backend-
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run database migrations

```bash
python3 -m alembic upgrade head
```

### 4. Start the server

```bash
python3 -m uvicorn main:app --reload
```

### 5. Open the interactive docs

```
http://127.0.0.1:8000/docs
```

---

## API Reference

### Auth

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/registerUser` | Register a new user | No |
| POST | `/api/v1/login` | Login and get JWT token | No |

### Notes

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/api/v1/getNotes` | Get all notes for current user | Yes |
| POST | `/api/v1/createNotes` | Create a new note | Yes |
| PUT | `/api/v1/updateNotes/{id}` | Update a note (partial update supported) | Yes |
| DELETE | `/api/v1/deleteNotes/{id}` | Delete a note | Yes |

---

## Authentication Flow

```
1. Register     POST /api/v1/registerUser   { username, password }
2. Login        POST /api/v1/login          { username, password }
3. Get token    ← { access_token, token_type: "bearer" }
4. Use token    Authorization: Bearer <token>  on all protected routes
```

---

## Key Design Decisions

**Ownership enforcement** — every note has an `owner_id` foreign key. On every read, update, and delete operation the API verifies the note belongs to the requesting user. Attempting to access another user's note returns `403 Forbidden`.

**Separate Pydantic schemas** — `CreateNotes`, `UpdateNotes`, and `NotesResponse` are intentionally separate. Clients never send `id`, `owner_id`, or timestamps — the server assigns these automatically.

**Partial updates** — `PUT` only updates fields that are explicitly sent. Omitted fields stay unchanged.

**Password security** — passwords are hashed with bcrypt before storage. Plain text passwords never touch the database.

---

## Environment Variables

For production, replace the hardcoded `SECRET_KEY` in `routers/user.py` with an environment variable:

```python
import os
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-dev-key")
```

---

## Database Schema

### users
| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| username | String | Unique username |
| hashed_password | String | bcrypt hashed password |

### notes
| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| title | String | Note title |
| content | String | Note content |
| owner_id | Integer | Foreign key → users.id |
| created_at | DateTime | Auto-set on create |
| updated_at | DateTime | Auto-updated on modify |

---

## License

MIT
