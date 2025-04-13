from uuid import UUID
from enum import Enum
from typing import List


class GenreEnum(str, Enum):
    horror = "Terror"
    comedy = "Comédia"
    romance = "Romance"
    drama = "Drama"
    action = "Ação"
    scifi = "Ficção Científica"


class Actor:
    id: UUID
    name: str


class Movie:
    id: UUID
    director_id: UUID
    actors: List[Actor]
    name: str
    genre: List[GenreEnum]
    average_rating: float = None


class Director:
    id: UUID
    name: str


class User:
    id: UUID
    email: str
    hashed_password: str


class UserMovie:
    user_id: UUID
    movie_id: UUID
    rating: float
