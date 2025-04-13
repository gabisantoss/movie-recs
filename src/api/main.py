from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Movie Recs API")

    return app


app = create_app()
