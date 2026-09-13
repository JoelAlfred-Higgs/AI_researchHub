from fastapi import FastAPI
from routers import notes
from routers import users


app = FastAPI()
app.include_router(notes.note_router)
app.include_router(users.user_router)
