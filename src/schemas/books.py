from typing import Optional

from pydantic import BaseModel


class BookSchema(BaseModel):
    id: Optional[int]
    title: str
    author: str
    reader_id: int

    class Config:
        orm_mode = True
