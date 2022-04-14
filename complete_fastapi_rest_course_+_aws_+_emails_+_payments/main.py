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
async def get_books(db: Session = Depends(get_db_connection)):
    return db.query(BookModel).all()
