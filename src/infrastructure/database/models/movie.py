import uuid

from sqlalchemy import Column, String, Float, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base

movie_actors = Table(
    "movie_actors",
    Base.metadata,
    Column("movie_id", UUID(as_uuid=True),
           ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", UUID(as_uuid=True),
           ForeignKey("actors.id"), primary_key=True),
)

movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", UUID(as_uuid=True),
           ForeignKey("movies.id"), primary_key=True),
    Column("genre", String, ForeignKey("genres.name"), primary_key=True),
)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    average_rating = Column(Float, nullable=True)

    director_id = Column(UUID(as_uuid=True), ForeignKey("directors.id"))
    director = relationship("Director", back_populates="movies")

    actors = relationship(
        "Actor", secondary=movie_actors, back_populates="movies")
    genres = relationship(
        "Genre", secondary=movie_genres, back_populates="movies")

    user_ratings = relationship("UserMovie", back_populates="movie")

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "average_rating": self.average_rating,
            "director": self.director.name if self.director else None,
            "genres": [genre.name for genre in self.genres]
        }
