from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


todos = [
    {
        "id": 1,
        "title": "Buy groceries",
        "completed": False
    },
    {
        "id": 2,
        "title": "Clean the house",
        "completed": True
    }
]


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: str
    completed: bool


@app.get("/todos")
def get_todos(completed: bool | None = None):

    if completed is None:
        return todos

    return [
        todo for todo in todos
        if todo["completed"] == completed
    ]




@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):

    for todo in todos:
        if todo["id"] == todo_id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: TodoCreate):

    new_todo = {
        "id": len(todos) + 1,
        "title": todo_data.title,
        "completed": False
    }

    todos.append(new_todo)

    return new_todo


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo_data: TodoUpdate):

    for todo in todos:
        if todo["id"] == todo_id:

            todo["title"] = todo_data.title
            todo["completed"] = todo_data.completed

            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    for todo in todos:
        if todo["id"] == todo_id:

            todos.remove(todo)

            return {
                "message": "Todo deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )