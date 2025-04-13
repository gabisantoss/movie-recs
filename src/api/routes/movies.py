
from typing import List
from fastapi import APIRouter
from src.repositories.movie_repository import MovieRepository
from src.infrastructure.database.session import SessionLocal

movie_router = APIRouter()
movie_repository = MovieRepository(SessionLocal())


@movie_router.get("/", response_model=List[dict])
def get_movies() -> List[dict]:
    """
        Get a list of all movies.
    """
    response = movie_repository.get_all()
    movies = []

    for movie in response:
        movies.append(movie.to_dict_summary())

    return movies
