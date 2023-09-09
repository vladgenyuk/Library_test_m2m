from datetime import date

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from backend.db.database import Base, metadata


class Reader(Base):
    __tablename__ = 'reader'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(length=100), nullable=True, unique=True)
    registered_at: date = Column(DateTime, default=func.now())
    first_name: str = Column(String(length=100), nullable=False)
    last_name: str = Column(String(length=100), nullable=False)
    surname: str = Column(String(length=100), nullable=False)

    books = relationship('ReadersBooks', back_populates='reader')


class Author(Base):
    __tablename__ = 'author'

    id: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(length=100), nullable=False)
    last_name: str = Column(String(length=100), nullable=False)

    books = relationship('AuthorsBooks', back_populates='author')
