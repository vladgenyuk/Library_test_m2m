from datetime import date

from pydantic import BaseModel, Field
from typing import List


class BookCreate(BaseModel):
    title: str
    authors: 'List[Author]'

    class Config:
        orm_mode = True


class Book(BookCreate):
    readers: 'List[ReaderCreate]'


class ReaderBook(BaseModel):
    issued_at: date
    returned_at: date
    book: 'BookCreate'
    reader: 'ReaderCreate'

    class Config:
        orm_mode = True


from .user import ReaderCreate, Author
Book.update_forward_refs()
BookCreate.update_forward_refs()
ReaderBook.update_forward_refs()
