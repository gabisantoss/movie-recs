from fastapi import FastAPI
from src.infrastructure.database.session import SessionLocal


def create_app() -> FastAPI:
    app = FastAPI(title="Movie Recs API")

    return app


app = create_app()
