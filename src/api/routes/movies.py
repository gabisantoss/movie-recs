
from uuid import UUID

from typing import List
from fastapi import APIRouter, HTTPException

from src.services.recommend_service import RecommendService

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


@movie_router.get("/{user_id}/recommendations", response_model=dict)
def get_movie_recommendations_by_user(user_id: UUID) -> dict:
    recommend_service = RecommendService()

    try:
        recommendations = recommend_service.recommend_movies(user_id)
        return {"user_id": user_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
