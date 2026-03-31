"""
FastAPI ToDo application using SQLite.

This app provides a simple CRUD API for managing ToDo items.
Each ToDo has an integer ID, content string, and a completed flag.
"""

from __future__ import annotations

from typing import Generator, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# ---------------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------------

# SQLite database URL (local file-based database)
DATABASE_URL = "sqlite:///./todos.db"

# Create the SQLAlchemy engine (check_same_thread needed for SQLite + threads)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy ORM models
Base = declarative_base()


# ---------------------------------------------------------------------------
# Database model
# ---------------------------------------------------------------------------


class TodoModel(Base):
    """SQLAlchemy model for the ToDo table."""

    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)


# Create tables on startup (simple local setup)
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------


class TodoBase(BaseModel):
    """Base schema shared by create/read."""

    content: str = Field(..., description="The text content of the todo item")
    completed: bool = Field(
        default=False, description="Completion status of the todo item"
    )


class TodoCreate(TodoBase):
    """Schema for creating a new ToDo."""


class TodoUpdate(BaseModel):
    """Schema for updating a ToDo (partial update via PUT)."""

    content: Optional[str] = Field(
        default=None, description="Updated text content of the todo item"
    )
    completed: Optional[bool] = Field(
        default=None, description="Updated completion status of the todo item"
    )


class Todo(TodoBase):
    """Schema returned to clients, including the primary key."""

    todo_id: int = Field(..., description="Unique identifier of the todo item")

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ToDo API",
    description="A simple FastAPI application to manage ToDo items using SQLite.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------


def get_db() -> Generator[Session, None, None]:
    """Provide a scoped database session per request."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/", summary="Root welcome endpoint")
def read_root() -> dict:
    """Return a basic welcome message."""

    return {"message": "Welcome to the FastAPI ToDo application!"}


@app.get("/todos", response_model=List[Todo], summary="Get all todos", tags=["todos"])
def get_all_todos(db: Session = Depends(get_db)) -> List[Todo]:
    """Retrieve all ToDo items."""

    return db.query(TodoModel).all()


@app.get(
    "/todos/{todo_id}",
    response_model=Todo,
    summary="Get a single todo by ID",
    tags=["todos"],
)
def get_todo(todo_id: int, db: Session = Depends(get_db)) -> Todo:
    """Retrieve a single ToDo item by its ID."""

    todo = db.query(TodoModel).filter(TodoModel.todo_id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )
    return todo


@app.post(
    "/todos",
    response_model=Todo,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
    tags=["todos"],
)
def create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    """Create a new ToDo item."""

    todo = TodoModel(content=todo_in.content, completed=todo_in.completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.put(
    "/todos/{todo_id}",
    response_model=Todo,
    summary="Update an existing todo",
    tags=["todos"],
)
def update_todo(todo_id: int, todo_in: TodoUpdate, db: Session = Depends(get_db)) -> Todo:
    """Update an existing ToDo item by its ID."""

    todo = db.query(TodoModel).filter(TodoModel.todo_id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )

    if todo_in.content is not None:
        todo.content = todo_in.content
    if todo_in.completed is not None:
        todo.completed = todo_in.completed

    db.commit()
    db.refresh(todo)
    return todo


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
    tags=["todos"],
)
def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a ToDo item by its ID."""

    todo = db.query(TodoModel).filter(TodoModel.todo_id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )

    db.delete(todo)
    db.commit()


