import uuid
import random
from sqlalchemy import text

from src.infrastructure.elastic.client import es
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
        movie_exists = session.query(Movie).first()
        if movie_exists:
            print("⏭ Seed skipped: data already exists in the database.")
            return

        session.execute(text(
            "TRUNCATE TABLE user_movies, movies, actors, directors, genres, users RESTART IDENTITY CASCADE"))
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
            session.add(movie)
            session.flush()

            es.index(
                index="movies",
                doc_type="movie",
                id=str(movie.id),
                body={
                    "id": str(movie.id),
                    "name": movie.name,
                    "average_rating": movie.average_rating,
                    "genres": [g.name for g in movie.genres],
                    "actors": [a.name for a in movie.actors],
                    "director": movie.director.name if movie.director else None
                }
            )

            movies.append(movie)
        session.add_all(movies)
        session.commit()

        user_list = [user1, user2, user3]
        for user in user_list:
            rated_movies = random.sample(movies, 10)
            for movie in rated_movies:
                rating_value = round(random.uniform(3.0, 5.0), 1)
                rating = UserMovie(user_id=user.id,
                                   movie_id=movie.id, rating=rating_value)
                session.add(rating)
                es.index(
                    index="ratings",
                    doc_type="rating",
                    id=f"{user.id}-{movie.id}",
                    body={
                        "user_id": str(user.id),
                        "movie_id": str(movie.id),
                        "rating": rating_value
                    }
                )

        session.commit()
