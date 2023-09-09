from datetime import datetime

from fastapi import APIRouter, Request, HTTPException, Query

from sqlalchemy import insert, update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, relationship

from backend.schemas.user import ReaderCreate, LoginReader
from backend.models import ReadersBooks, Book, AuthorsBooks, Author, Reader
from backend.crud.user_crud import user

router = APIRouter()


@router.get('/reader_by_id')
async def get_reader_by_id(
        request: Request,
        id: int
):
    session: AsyncSession = request.state.db_session
    reader = await user.get_user_by_id(session, id)
    return reader


@router.get('/readers')
async def get_all_readers(
        request: Request
):
    session: AsyncSession = request.state.db_session
    users = await user.get_users(session)
    return users


@router.post('/auth')
async def login_reader(
        request: Request,
        login: LoginReader
):
    session: AsyncSession = request.state.db_session
    reader = await user.login_user(session=session, email=login.email, first_name=login.first_name)
    if not reader:
        raise HTTPException(status_code=404, detail='User with this email does not exists, please register'
                                                    ', or you entered wrong first name, please try again')

    request.session['current_reader'] = reader.id
    return reader.id


@router.post('/register')
async def register_reader(
        request: Request,
        new_reader: ReaderCreate
):
    new_reader = new_reader.dict()
    session: AsyncSession = request.state.db_session
    try:
        reader = await user.register_user(session=session, user_data=new_reader)
        request.session['current_reader'] = reader.id
        return reader
    except IntegrityError:
        raise HTTPException(status_code=409, detail='User with that email already exists')


@router.put('/borrow')
async def borrow_book(
        request: Request,
        book_id: int
):
    if not request.session.get('current_reader'):
        raise HTTPException(
            status_code=401,
            detail='Authorize first to get access to borrow books'
        )
    session: AsyncSession = request.state.db_session
    try:
        stmt = select(Book).where(Book.id == book_id)
        book = (await session.execute(stmt)).scalar_one_or_none()
        if book and book.status == "Borrowed":
            raise HTTPException(status_code=404, detail='This book already borrowed')
        stmt = update(Book).\
            values(status='Borrowed').\
            where(and_(Book.id == book_id, Book.status == 'In Library'))
        await session.execute(stmt)
        stmt = insert(ReadersBooks).values(reader_id=request.session.get('current_reader'), book_id=book_id)
        await session.execute(stmt)
        await session.commit()
        return {'borrowed_at': datetime.now()}

    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail='This book does not exist')


@router.put('/return')
async def return_book(
        request: Request,
        book_id: int,
):
    if not request.session.get('current_reader'):
        raise HTTPException(
            status_code=401,
            detail='Authorize first to get access to borrow books'
        )
    session: AsyncSession = request.state.db_session
    stmt = update(ReadersBooks).\
        values(returned_at=datetime.now()).\
        where(
        and_(
            ReadersBooks.book_id == book_id,
            ReadersBooks.reader_id == request.session.get('current_reader')
        ))
    await session.execute(stmt)
    stmt = update(Book).values(status='In library').where(Book.id == book_id)
    await session.execute(stmt)
    await session.commit()
    return {'returned_at': datetime.now()}


@router.get('/available')
async def get_available_books(
        request: Request,
        my_id: int = None
):
    my_id = my_id or request.session.get('current_reader')
    if not my_id:
        raise HTTPException(status_code=401, detail="Please Authorize first to get access to library")
    session: AsyncSession = request.state.db_session
    stmt = select(Book, Author).\
        select_from(Book).\
        join(AuthorsBooks, Book.id == AuthorsBooks.book_id).\
        join(Author, Author.id == AuthorsBooks.author_id, isouter=True).\
        where(Book.status == "In Library")
    results = await session.execute(stmt)
    results = results.unique().all()
    hashset = {}
    for r in results:
        data = dict(r._mapping)
        book = data['Book']
        author = data['Author']
        if not book.id in hashset:
            hashset[book.id] = []
            hashset[book.id].append(book.title)
        hashset[book.id].append(author)
    return hashset


@router.get('/my_books')
async def get_my_books(
        request: Request,
        my_id: int = None
):
    my_id = my_id or request.session.get('current_reader')
    if not my_id:
        raise HTTPException(status_code=401, detail="please authorize first to get access to your books")
    session: AsyncSession = request.state.db_session
    stmt = select(Book, Author).\
        select_from(Book).\
        join(AuthorsBooks, Book.id == AuthorsBooks.book_id).\
        join(Author, Author.id == AuthorsBooks.author_id, isouter=True).\
        join(ReadersBooks).\
        where(and_(Book.status == "Borrowed", ReadersBooks.reader_id == my_id))
    results = await session.execute(stmt)
    results = results.unique().all()
    hashset = {}
    for r in results:
        data = dict(r._mapping)
        book = data['Book']
        author = data['Author']
        if not book.id in hashset:
            hashset[book.id] = []
            hashset[book.id].append(book.title)
        hashset[book.id].append(author)
    return hashset
