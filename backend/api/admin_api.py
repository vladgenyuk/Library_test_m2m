from fastapi import APIRouter, Request
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import and_, select, insert, func

from backend.schemas.book import BookCreate
from backend.models import Book, Author, AuthorsBooks, ReadersBooks, Reader


router = APIRouter()


@router.get('/book_count')
async def get_total_books_count(
        request: Request
):
    session: AsyncSession = request.state.db_session
    stmt = select(func.count()).select_from(Book)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


@router.post('/create_book')
async def create_book(
        request: Request,
        new_book: BookCreate,
):
    session: AsyncSession = request.state.db_session
    book_data = new_book.dict()

    first = []
    last = []
    for i in book_data['authors']:
        first.append(i['first_name'])
        last.append(i['last_name'])

    stmt = select(Author).filter(and_(
        Author.first_name.in_(first),
        Author.last_name.in_(last)
    ))

    results = await session.execute(stmt)

    authors_in_db = {
        f'{i.first_name+i.last_name}': i.id
    for i in results.scalars()}

    book_obj = Book(title=book_data['title'])
    await session.execute(stmt)
    session.add(book_obj)
    await session.commit()

    new_authors_books = []
    for i in book_data['authors']:
        full_name = i['first_name'] + i['last_name']
        if authors_in_db.get(full_name):
            author_book_obj = AuthorsBooks(book_id=book_obj.id, author_id=authors_in_db.get(full_name))
        else:
            author_obj = Author(first_name=i['first_name'], last_name=i['last_name'])
            session.add(author_obj)
            await session.commit()
            author_book_obj = AuthorsBooks(book_id=book_obj.id, author_id=author_obj.id)

        new_authors_books.append(author_book_obj)
    session.add_all(new_authors_books)
    await session.commit()
    return book_data


@router.get('/stats')
async def get_borrowed_stats(
        request: Request,
        id: int
):
    session: AsyncSession = request.state.db_session
    stmt = select(ReadersBooks, Book, Reader).\
        select_from(ReadersBooks).\
        join(Reader).\
        join(Book).\
        where(Reader.id == id)

    result = await session.execute(stmt)
    return [dict(r._mapping) for r in result.all()]
