from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import init_db, get_connection
app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks.",
    version="1.0.0"
    )
init_db()
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Learn Git", "done": True},
]


@app.get("/")
def root():
   return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/tasks")
def get_tasks():
    connection = get_connection()

    rows = connection.execute(
        "SELECT id, title, done FROM tasks"
    ).fetchall()

    connection.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }
        for row in rows
    ]
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }
class TaskCreate(BaseModel):
    title: str
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, False)
    )
    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "id": task_id,
        "title": task.title,
        "done": False
    }

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    connection = get_connection()

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if row is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    new_title = task_update.title if task_update.title is not None else row[1]
    new_done = task_update.done if task_update.done is not None else bool(row[2])

    if not new_title.strip():
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (new_title, new_done, task_id)
    )

    connection.commit()
    connection.close()

    return {
        "id": task_id,
        "title": new_title,
        "done": new_done
    }

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if row is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()