import os
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware


load_dotenv()
middleware_key = os.getenv("MIDDLEWARE_SECRET_KEY")

if not middleware_key:
    raise RuntimeError("MIDDLEWARE_SECRET_KEY is missing")


app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=middleware_key,
    max_age=86400,
    https_only=True
)

@app.get("/")
def root():
    return {"message" : "Hello World"}


@app.get("/session_test")
async def session(request: Request):
    session = request.session

    if "test_counter" not in session:
        session["test_counter"] = 0

    session["test_counter"] += 1

    return {"test_counter" : session["test_counter"]}
