from typing import Optional

from pydantic import BaseModel


class ReaderSchema(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
