from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base
from src.infrastructure.database.models.movie import movie_genres


class Genre(Base):
    __tablename__ = "genres"

    name = Column(String, primary_key=True)

    movies = relationship(
        "Movie", secondary=movie_genres, back_populates="genres")
