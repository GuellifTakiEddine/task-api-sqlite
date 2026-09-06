# Task API — SQLite

A CRUD API built with Python, FastAPI, and SQLite.

## Why SQLite?

SQLite was chosen because it is lightweight and does not require a separate database server.
The database is stored in a single file called `tasks.db`.

## Database

The database file is:

`tasks.db`

The `tasks` table contains:

- `id` — integer primary key
- `title` — text
- `done` — boolean

The database and table are created automatically when the application starts.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate

Install the dependencies:
pip install -r requirements.txt

Run the API
fastapi dev main.py

The API is available at:

http://127.0.0.1:8000

API Endpoints
Method	Endpoint	    Description
GET	        /	        API information
GET	    /health	        Health check
GET	    /tasks	        Get all tasks
GET	    /tasks/{id}	    Get one task
POST	/tasks	        Create a task
PUT	    /tasks/{id}	    Update a task
DELETE	/tasks/{id}	    Delete a task

Example SQL Query:
SELECT * FROM tasks WHERE done = 1;

Swagger UI

Interactive API documentation:

http://127.0.0.1:8000/docs

Database Screenshot

```text
docs/database.png