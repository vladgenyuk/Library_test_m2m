from datetime import date

from sqlalchemy import Column, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import relationship

from backend.db.database import Base, metadata


class ReadersBooks(Base):
    __tablename__ = 'readers_books'
    id: int = Column(Integer, primary_key=True)
    book_id: int = Column(Integer, ForeignKey('book.id'), default=1)
    reader_id: int = Column(Integer, ForeignKey('reader.id'), default=1)
    book = relationship("Book", back_populates="readers")
    reader = relationship("Reader", back_populates="books")

    issued_at: date = Column(DateTime, default=func.now())
    returned_at: date = Column(DateTime, default=None)


class AuthorsBooks(Base):
    __tablename__ = 'authors_books'

    author_id: int = Column(Integer, ForeignKey('author.id'), primary_key=True, default=1)
    book_id: int = Column(Integer, ForeignKey('book.id'), primary_key=True, default=1)
    author = relationship("Author", back_populates="books")
    book = relationship("Book", back_populates="authors")
