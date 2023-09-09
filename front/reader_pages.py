import httpx

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory='front/templates')


@router.get('/stats')
async def get_user_stats_pages(
        request: Request,
):
    if not request.session.get('current_reader'):
        return RedirectResponse(f'http://127.0.0.1:8000/reader_pages/register')
    async with httpx.AsyncClient() as client:
        stats = await client.get(
            f'http://127.0.0.1:8000/admin/stats?id={request.session.get("current_reader")}'
        )
        stats = stats.json()
        return templates.TemplateResponse('stats.html', {'request': request, 'stats': stats})


@router.get('/available_books')
async def get_available_books_pages(
        request: Request
):

    if not request.session.get('current_reader'):
        return RedirectResponse(f'http://127.0.0.1:8000/reader_pages/register')
    async with httpx.AsyncClient() as client:
        books = await client.get(
            f'http://127.0.0.1:8000/reader/available?my_id={request.session.get("current_reader")}'
        )
        books = books.json()
    return templates.TemplateResponse('available_books.html', {'request': request, 'books': books})


@router.get('/my_books')
async def return_pages(
        request: Request
):
    if not request.session.get('current_reader'):
        return RedirectResponse('http://127.0.0.1:8000/reader_pages/register')
    async with httpx.AsyncClient() as client:
        books = await client.get(
            f'http://127.0.0.1:8000/reader/my_books?my_id={request.session.get("current_reader")}'
        )
        reader = await client.get(
            f'http://127.0.0.1:8000/reader/reader_by_id?id={request.session.get("current_reader")}'
        )
        reader = reader.json()
        books = books.json()
    return templates.TemplateResponse('my_books.html', {'request': request, 'books': books, 'reader': reader})


@router.get('/register')
async def register_reader_pages(
        request: Request,
):
    return templates.TemplateResponse('register.html', {'request': request})


@router.get('/login/{email}')
async def login_reader_pages(
        request: Request,
        email: str
):
    return templates.TemplateResponse('login.html', {'request': request, 'email': email})


@router.get('/readers_list')
async def readers_list_pages(
        request: Request
):
    async with httpx.AsyncClient() as client:
        readers = await client.get(
            f'http://127.0.0.1:8000/reader/readers'
        )
        readers = readers.json()
    return templates.TemplateResponse('readers_list.html', {'request': request, 'readers': readers})
