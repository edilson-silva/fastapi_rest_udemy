from typing import List

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import delete
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
async def books_get(book_id: int, db: Session = Depends(get_db_connection)):
    return db.query(BookModel).filter(BookModel.id == book_id).first()


@app.post("/books")
async def books_create(book: BookSchema, db: Session = Depends(get_db_connection)):
    book_model = BookModel(**book.dict())
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model


@app.put("/books/{book_id}")
async def books_update(
    book_id: int, book: BookSchema, db: Session = Depends(get_db_connection)
):
    book = book.dict()
    del book["id"]

    updated = db.query(BookModel).filter(BookModel.id == book_id).update(values=book)
    db.commit()

    if updated:
        return {"message": "book updated"}

    return JSONResponse(content={"message": "book not found"}, status_code=404)


@app.delete("/books/{book_id}")
async def books_delete(book_id: int, db: Session = Depends(get_db_connection)):
    deleted = db.query(BookModel).filter(BookModel.id == book_id).delete()
    db.commit()

    if deleted:
        return {"message": "book deleted"}

    return JSONResponse(content={"message": "book not found"}, status_code=404)
