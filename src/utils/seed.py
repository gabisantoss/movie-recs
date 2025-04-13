import uuid
import random

from src.infrastructure.database.session import SessionLocal

from src.infrastructure.database.models.user_movie import UserMovie
from src.infrastructure.database.models.movie import Movie
from src.infrastructure.database.models.actor import Actor
from src.infrastructure.database.models.director import Director
from src.infrastructure.database.models.genre import Genre
from src.infrastructure.database.models.user import User


def seed_data():
    print("🌱 Seeding database with dummy data...")
    with SessionLocal() as session:
        session.query(UserMovie).delete()
        session.query(Movie).delete()
        session.query(Actor).delete()
        session.query(Director).delete()
        session.query(Genre).delete()
        session.query(User).delete()
        session.commit()

        genre_names = ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller"]
        genres = [Genre(name=name) for name in genre_names]
        session.add_all(genres)

        director_names = ["Christopher Nolan",
                          "Quentin Tarantino", "Greta Gerwig", "Martin Scorsese"]
        directors = [Director(name=name) for name in director_names]
        session.add_all(directors)

        actor_names = [
            "Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page", "Brad Pitt",
            "Margot Robbie", "Saoirse Ronan", "Robert De Niro", "Timothée Chalamet",
            "Zendaya", "Tom Hardy"
        ]
        actors = [Actor(name=name) for name in actor_names]
        session.add_all(actors)

        user1 = User(id=uuid.uuid4(), email="user1@example.com")
        user2 = User(id=uuid.uuid4(), email="user2@example.com")
        user3 = User(id=uuid.uuid4(), email="user3@example.com")
        session.add_all([user1, user2, user3])

        session.commit()

        movies = []
        for i in range(1, 31):
            movie = Movie(
                name=f"Movie {i}",
                average_rating=round(random.uniform(2.5, 5.0), 1),
                director=random.choice(directors),
                genres=random.sample(genres, k=random.randint(1, 2)),
                actors=random.sample(actors, k=random.randint(2, 4))
            )
            movies.append(movie)
        session.add_all(movies)
        session.commit()

        user_list = [user1, user2, user3]
        for user in user_list:
            rated_movies = random.sample(movies, 10)
            for movie in rated_movies:
                rating = round(random.uniform(3.0, 5.0), 1)
                session.add(UserMovie(user_id=user.id,
                            movie_id=movie.id, rating=rating))

        session.commit()
