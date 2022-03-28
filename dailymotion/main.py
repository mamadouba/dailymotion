#!/bin/python3
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dailymotion.endpoints import users
from dailymotion.db import Database
from dailymotion.settings import settings


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users.router)

    @app.get("/")
    def root():
        return {"detail": "Daily Motion"}

    @app.exception_handler(Exception)
    def exception_handler(request: Request, exc: Exception):
        print(exc)
        return JSONResponse({"detail": "internal server error"}, status_code=500)

    return app


app = create_app()
