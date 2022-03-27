#!/bin/python3
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dailymotion.endpoints import users
from dailymotion.dependancies import get_db
revoked_tokens: dict = {}


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

    @app.on_event("startup")
    def startup_event():
        db = get_db()
        #db.drop_tables()
        db.create_tables()


    return app


app = create_app()
