from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# ----------------------------
# Pydantic model (schema)
# ----------------------------
class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    status: str = Field("pending", pattern="^(pending|in_progress|completed)$")

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=200)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")

# ----------------------------
# Fake "database" (in-memory list)
# ----------------------------
tasks: List[Task] = []
next_id = 1

# ----------------------------
# Endpoints
# ----------------------------

# Create a task (POST)
@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    global next_id
    new_task = Task(id=next_id, title=task.title, description=task.description)
    tasks.append(new_task)
    next_id += 1
    return new_task

# Get all tasks (GET)
@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks

# Get a single task (GET)
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Update a task (PUT)
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, update: TaskUpdate):
    for task in tasks:
        if task.id == task_id:
            if update.title is not None:
                task.title = update.title
            if update.description is not None:
                task.description = update.description
            if update.status is not None:
                task.status = update.status
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Delete a task
@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"message": f"Task {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
