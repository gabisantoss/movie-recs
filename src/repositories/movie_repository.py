from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from src.infrastructure.database.models.movie import Movie


class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Movie]:
        return self.db.query(Movie).all()

    def get_by_id(self, movie_id: UUID) -> Movie:
        return self.db.get(movie_id)
