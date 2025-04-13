from sqlalchemy import Column, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base


class UserMovie(Base):
    __tablename__ = "user_movies"

    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), primary_key=True)
    movie_id = Column(UUID(as_uuid=True), ForeignKey(
        "movies.id"), primary_key=True)
    rating = Column(Float, nullable=False)

    user = relationship("User", back_populates="rated_movies")
    movie = relationship("Movie", back_populates="user_ratings")
