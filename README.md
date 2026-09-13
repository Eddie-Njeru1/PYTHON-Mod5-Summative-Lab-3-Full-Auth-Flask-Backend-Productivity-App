# Notes API — Full Auth Flask Backend

This is a backend API for a notes app, built with Flask, SQLAlchemy, and JWT authentication. It allows users to sign up, log in, and manage their own private notes. Every note is scoped to the user who created it, and no user can view or modify another user's notes.

## Features

- Sign up and log in with JWT-based authentication.
- Create, view, update, and delete notes via REST API.
- Notes are paginated when listed.
- Passwords are hashed with bcrypt and never stored or returned in plaintext.
- Every notes route checks ownership. A note that isn't yours returns a 404, not its contents.

## Project Structure

```
PYTHON-Mod5-Summative-Lab-3-Full-Auth-Flask-Backend-Productivity-App/
├── app.py              # Flask app factory, config, and extension setup
├── extensions.py       # Shared db, bcrypt, migrate, and jwt instances
├── models.py           # User and Note SQLAlchemy models
├── routes.py           # All API routes (auth + notes)
├── seed.py             # Sample data for the database
├── migrations/         # Flask-Migrate/Alembic migration scripts
├── requirements.txt    # For deployment platforms that don't use pipenv
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Data Model

- **User** — id, username (unique), password_hash (hashed via bcrypt, never exposed)
- **Note** — id, title, content, user_id (foreign key to User)
- A User has many Notes. Deleting a user also deletes their notes.
- Data is persisted in SQLite locally (`app.db`) and PostgreSQL in production, so it survives server restarts.

## Prerequisites

- Python 3.x (This project was done on Python 3.14.6)
- Pipenv

## Installation and Dependencies

Clone the repository and set up the environment:

```bash
git clone https://github.com/Eddie-Njeru1/PYTHON-Mod5-Summative-Lab-3-Full-Auth-Flask-Backend-Productivity-App.git
cd PYTHON-Mod5-Summative-Lab-3-Full-Auth-Flask-Backend-Productivity-App
pipenv install       # installs all project dependencies and creates the virtual environment
pipenv shell         # launches the virtual environment
```

The Pipfile defines the project's dependencies, while Pipfile.lock ensures consistent package versions across different development environments.

- `flask` — powers the REST API and routing.
- `flask-sqlalchemy` — ORM layer connecting Flask to the database.
- `flask-migrate` — manages database schema migrations.
- `flask-bcrypt` — hashes and verifies passwords.
- `flask-jwt-extended` — issues and verifies JWTs for authentication.
- `flask-cors` — allows the separately-hosted frontend client to call this API.
- `python-dotenv` — loads local environment variables from a `.env` file.

**Note on Python version:** the versions originally specified for this lab (Flask 2.2.2, Werkzeug 2.2.2) rely on standard library functions (`ast.Str`, `pkgutil.get_loader`) that were removed in Python 3.14. This project uses Flask 3.1.2 instead, which resolves the incompatibility with no other code changes needed.

Set up and seed the database:

```bash
flask db init        # first-time only
flask db migrate -m "initial migration"
flask db upgrade
pipenv run python seed.py
```

Seeding creates 3 sample users, each with 4 notes. All seeded users share the password `password123`.

(Optional) create a `.env` file in the project root to turn off Flask's debug mode locally:
```
APP_DEBUG=false
```

## Running the Application

Start the Flask server:

```bash
python3 app.py
```

The API runs at `http://localhost:5555`.

A live deployed version is also available at:
https://python-mod5-summative-lab-3-full-auth.onrender.com

(Hosted on Render's free tier — if it's been idle for 15+ minutes, the first request takes 30–60 seconds to wake up.)

## Sign Up

```bash
curl -X POST http://localhost:5555/signup -H "Content-Type: application/json" -d '{"username": "eddie", "password": "pw123"}'
```

## Log In

```bash
curl -X POST http://localhost:5555/login -H "Content-Type: application/json" -d '{"username": "eddie", "password": "pw123"}'
```

Both return a JSON object with a `token` — use it as `Authorization: Bearer <token>` on every request below.

## Get Current User

```bash
curl http://localhost:5555/me -H "Authorization: Bearer <token>"
```

## View All Notes (paginated)

```bash
curl "http://localhost:5555/notes?page=1&per_page=10" -H "Authorization: Bearer <token>"
```

## Create a Note

```bash
curl -X POST http://localhost:5555/notes -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"title": "Groceries", "content": "Milk, eggs"}'
```

## Update a Note

```bash
curl -X PATCH http://localhost:5555/notes/1 -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"title": "Updated title"}'
```

## Delete a Note

```bash
curl -X DELETE http://localhost:5555/notes/1 -H "Authorization: Bearer <token>"
```

Note: all `/notes` routes require a valid token and only ever return or affect notes owned by the authenticated user. Trying to access or edit another user's note returns a 404, the same as if the note didn't exist at all.

## Validations

- **Table constraints (database level):** `User.username` is unique and required; `Note.title`, `Note.content`, and `Note.user_id` are all required (not null); `Note.user_id` is a foreign key into `User`.
- **Route-level validation:** signup/login reject a missing username or password (400); signup rejects a username that's already taken (400); note creation rejects a missing title or content (400).
- This project does not use a schema library (e.g. Marshmallow) for validation. Request data is checked directly in `routes.py`.

## Current Limitations

The current version intentionally keeps the feature set to what's required.

- There's no endpoint to update a username or password, or delete a user account.
- JWTs expire with no refresh-token flow. Once expired, the user has to log in again.
- No automated test suite is included; all endpoints were tested manually with curl.

## Frontend

A pre-built React client for testing this API (JWT and session versions) is available at:
https://github.com/learn-co-curriculum/flask-c10-summative-lab-sessions-and-jwt-clients

Use the `client-with-jwt` folder to match this project's auth method.