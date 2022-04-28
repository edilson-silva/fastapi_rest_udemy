from sqlalchemy import Column, Integer, String
from src.connection.database import Base


class ReaderModel(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
