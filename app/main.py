from fastapi import FastAPI
from app.routers import auth
from app.routers import books
from app.routers import readers
from app.routers import borrow
from app.routers import users

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(borrow.router)
app.include_router(users.router)



