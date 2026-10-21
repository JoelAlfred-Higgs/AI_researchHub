from contextlib import asynccontextmanager

from fastapi import FastAPI
from .DataBase import dispose_database, validate_database_config
from .routers import notes, users, categories
from .security import validate_security_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_database_config()
    validate_security_config()
    yield
    dispose_database()


app = FastAPI(lifespan=lifespan)
app.include_router(users.user_router,prefix="/users")
app.include_router(categories.categ_router,prefix = "/categories")
app.include_router(notes.note_router, prefix="/notes")
