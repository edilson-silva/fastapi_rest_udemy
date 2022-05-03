from sqlalchemy import Column, ForeignKey, Integer
from src.connection.database import Base


class ReaderBookModel(Base):
    __tablename__ = "readers_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(ForeignKey("books.id"), nullable=False)
    reader_id = Column(ForeignKey("readers.id"), nullable=False)
