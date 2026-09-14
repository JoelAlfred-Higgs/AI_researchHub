from fastapi import FastAPI
from routers import notes
from routers import users
from routers import categories


app = FastAPI()
app.include_router(notes.note_router,prefix="/notes")
app.include_router(users.user_router,prefix="/users")
app.include_router(categories.categ_router,prefix = "/categories")