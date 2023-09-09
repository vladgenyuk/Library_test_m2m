from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

from backend.db.database import async_session_maker
from backend.api import admin_router, reader_router

from front.reader_pages import router as reader_pages

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key='secret')


@app.get('')
async def home():
    return {'Hello': 'World'}


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    request.state.db_session = async_session_maker()
    response = await call_next(request)
    await request.state.db_session.close()
    return response


app.include_router(
    admin_router,
    prefix='/admin',
    tags=['admin']
)


app.include_router(
    reader_router,
    prefix='/reader',
    tags=['reader']
)

app.include_router(
    reader_pages,
    prefix='/reader_pages',
    tags=['reader_pages']
)
