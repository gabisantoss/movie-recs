from fastapi import FastAPI
from src.api.routes.movies import movie_router


def create_app() -> FastAPI:
    app = FastAPI(title="Movie Recs API")

    app.include_router(movie_router, prefix="/movies")

    return app


app = create_app()
