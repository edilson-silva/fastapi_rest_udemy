from typing import Optional

from pydantic import BaseModel


class BookModel(BaseModel):
    id: Optional[int]
    title: str
    author: str

    class Config:
        orm_mode: True
