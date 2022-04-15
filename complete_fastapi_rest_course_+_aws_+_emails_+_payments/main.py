from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .connection.database import get_db_connection
from .models.books import BookModel
from .schemas.books import BookSchema

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Welcome to API!"}


@app.get("/books", response_model=List[BookSchema])
async def books_list(db: Session = Depends(get_db_connection)):
    return db.query(BookModel).all()


@app.get("/books/{book_id}", response_model=BookSchema)
async def books_list(book_id: int, db: Session = Depends(get_db_connection)):
    return db.query(BookModel).filter(BookModel.id == book_id).first()


@app.post("/books")
async def books_create(book: BookSchema, db: Session = Depends(get_db_connection)):
    book_model = BookModel(**book.dict())
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model
