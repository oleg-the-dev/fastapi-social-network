from fastapi import FastAPI

from endpoints import auth, posts, users

app = FastAPI(title="Simple RESTful API for a social networking application")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
