from typing import Optional

from pydantic import BaseModel


class ReaderBookSchema(BaseModel):
    id: Optional[int]
    book_id: int
    reader_id: int

    class Config:
        orm_mode = True
