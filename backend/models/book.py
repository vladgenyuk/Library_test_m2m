from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from typing import Literal

from .association import ReadersBooks, AuthorsBooks
from backend.db.database import Base, metadata


class Book(Base):
    __tablename__ = 'book'

    id: int = Column(Integer, primary_key=True)
    title: int = Column(String(length=100), nullable=False)
    status: Literal['In library', 'Borrowed'] = Column(String(length=20), default='In library')

    readers = relationship('ReadersBooks', back_populates='book')
    authors = relationship('AuthorsBooks', back_populates='book')

    def __str__(self):
        return self.title
