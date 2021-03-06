from typing import List

from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.auth.crypt import Crypt
from src.auth.custom_http_header_handler import CustomHTTPHeaderHandler
from src.auth.token import generate_token
from src.connection.database import get_db_connection, init_db
from src.models.books import BookModel
from src.models.readers import ReaderModel
from src.models.readers_books import ReaderBookModel
from src.models.users import UserModel
from src.schemas.books import BookSchema
from src.schemas.readers import ReaderSchema
from src.schemas.readers_books import ReaderBookSchema
from src.schemas.users import UserRegisterSchema

app = FastAPI()
oauth2_scheme = CustomHTTPHeaderHandler()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
async def home():
    return {"message": "Welcome to API!"}


@app.get("/books", response_model=List[BookSchema])
async def books_list(db: Session = Depends(get_db_connection)):
    return db.query(BookModel).all()


@app.get("/books/{book_id}", response_model=BookSchema)
async def books_get(book_id: int, db: Session = Depends(get_db_connection)):
    return db.query(BookModel).filter(BookModel.id == book_id).first()


@app.post("/books", dependencies=[Depends(oauth2_scheme)])
async def books_create(book: BookSchema, db: Session = Depends(get_db_connection)):
    book_model = BookModel(**book.dict())
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model


@app.put("/books/{book_id}", dependencies=[Depends(oauth2_scheme)])
async def books_update(
    book_id: int, book: BookSchema, db: Session = Depends(get_db_connection)
):
    book = book.dict()
    del book["id"]

    updated = db.query(BookModel).filter(BookModel.id == book_id).update(values=book)
    db.commit()

    if updated:
        return {"message": "book updated"}

    return JSONResponse(
        content={"message": "book not found"}, status_code=status.HTTP_404_NOT_FOUND
    )


@app.delete("/books/{book_id}", dependencies=[Depends(oauth2_scheme)])
async def books_delete(book_id: int, db: Session = Depends(get_db_connection)):
    deleted = db.query(BookModel).filter(BookModel.id == book_id).delete()
    db.commit()

    if deleted:
        return {"message": "book deleted"}

    return JSONResponse(
        content={"message": "book not found"}, status_code=status.HTTP_404_NOT_FOUND
    )


@app.get(
    "/readers", response_model=List[ReaderSchema], dependencies=[Depends(oauth2_scheme)]
)
async def readers_list(db: Session = Depends(get_db_connection)):
    return db.query(ReaderModel).all()


@app.get(
    "/readers/{reader_id}",
    response_model=ReaderSchema,
    dependencies=[Depends(oauth2_scheme)],
)
async def readers_get(reader_id: int, db: Session = Depends(get_db_connection)):
    return db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()


@app.post("/readers", dependencies=[Depends(oauth2_scheme)])
async def readers_create(
    reader: ReaderSchema, db: Session = Depends(get_db_connection)
):
    reader_model = ReaderModel(**reader.dict())
    db.add(reader_model)
    db.commit()
    db.refresh(reader_model)
    return reader_model


@app.put("/readers/{reader_id}", dependencies=[Depends(oauth2_scheme)])
async def readers_update(
    reader_id: int, reader: ReaderSchema, db: Session = Depends(get_db_connection)
):
    reader = reader.dict()
    del reader["id"]

    updated = (
        db.query(ReaderModel).filter(ReaderModel.id == reader_id).update(values=reader)
    )
    db.commit()

    if updated:
        return {"message": "reader updated"}

    return JSONResponse(
        content={"message": "reader not found"}, status_code=status.HTTP_404_NOT_FOUND
    )


@app.delete("/readers/{reader_id}", dependencies=[Depends(oauth2_scheme)])
async def readers_delete(reader_id: int, db: Session = Depends(get_db_connection)):
    deleted = db.query(ReaderModel).filter(ReaderModel.id == reader_id).delete()
    db.commit()

    if deleted:
        return {"message": "reader' deleted"}

    return JSONResponse(
        content={"message": "reader not found"}, status_code=status.HTTP_404_NOT_FOUND
    )


@app.post("/readers_books", dependencies=[Depends(oauth2_scheme)])
async def readers_books_create(
    reader_book: ReaderBookSchema, db: Session = Depends(get_db_connection)
):
    try:
        reader_book_model = ReaderBookModel(**reader_book.dict())
        db.add(reader_book_model)
        db.commit()
        db.refresh(reader_book_model)
        return reader_book_model
    except IntegrityError:
        return JSONResponse(
            content={"message": "send a valid reader and book ids"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@app.post(
    "/users", dependencies=[Depends(oauth2_scheme), Depends(oauth2_scheme.is_admin)]
)
async def users_create(
    user: UserRegisterSchema, db: Session = Depends(get_db_connection)
):
    found_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if found_user:
        return JSONResponse(
            content={"message": "email already in use"},
            status_code=status.HTTP_409_CONFLICT,
        )

    crypt = Crypt()
    user.password = crypt.get_hashed_password(user.password)

    user_model = UserModel(**user.dict())
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return {"token": generate_token(user_model)}
