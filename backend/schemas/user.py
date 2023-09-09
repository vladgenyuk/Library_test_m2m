from datetime import date

from pydantic import BaseModel, EmailStr
from typing import List

from .book import BookCreate


class Author(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class ReaderCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    surname: str

    class Config:
        orm_mode = True


class Reader(ReaderCreate):
    id: int
    registered_at: date
    books: 'List[BookCreate]'


class LoginReader(BaseModel):
    email: EmailStr
    first_name: str
