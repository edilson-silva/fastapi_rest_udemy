from sqlalchemy import Column, ForeignKey, Integer, String
from src.connection.database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    reader_id = Column(ForeignKey("readers.id"), nullable=False, index=True)
