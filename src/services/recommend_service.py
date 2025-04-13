from src.infrastructure.elastic.client import es
from uuid import UUID


class RecommendService:
    def __init__(self, movie_index: str = "movies", rating_index: str = "ratings"):
        self.movie_index = movie_index
        self.rating_index = rating_index

    def get_user_rated_movies(self, user_id: UUID) -> list[str]:
        """Fetch movie_ids rated by the user."""
        resp = es.search(index=self.rating_index, size=1000, body={
            "query": {
                "bool": {
                    "must": [
                        {"term": {"user_id": str(user_id)}}
                    ]
                }
            }
        })

        return [hit["_source"]["movie_id"] for hit in resp["hits"]["hits"]]

    def get_similar_users(self, user_id: UUID) -> list[str]:
        """Find users who rated same movies."""
        rated_movies = self.get_user_rated_movies(user_id)
        if not rated_movies:
            return []

        resp = es.search(index=self.rating_index, size=1000, body={
            "query": {
                "bool": {
                    "must": [
                        {"terms": {"movie_id": rated_movies}},
                        {"bool": {"must_not": {
                            "term": {"user_id": str(user_id)}}}}
                    ]
                }
            }
        })

        return list(set([hit["_source"]["user_id"] for hit in resp["hits"]["hits"]]))

    def recommend_movies(self, user_id: UUID, size: int = 10) -> list[dict]:
        """Recommend movies based on similar users' high ratings."""
        rated_movies = set(self.get_user_rated_movies(user_id))
        similar_users = self.get_similar_users(user_id)

        if not similar_users:
            # fallback to top-rated movies
            return self.recommend_top_rated(exclude=rated_movies)

        resp = es.search(index=self.rating_index, size=1000, body={
            "query": {
                "bool": {
                    "must": [
                        {"terms": {"user_id": similar_users}},
                        {"range": {"rating": {"gte": 4.0}}}
                    ]
                }
            }
        })

        movie_scores = {}
        for hit in resp["hits"]["hits"]:
            movie_id = hit["_source"]["movie_id"]
            if movie_id not in rated_movies:
                movie_scores[movie_id] = movie_scores.get(movie_id, 0) + 1

        top_movie_ids = sorted(
            movie_scores, key=movie_scores.get, reverse=True)[:size]
        return self.fetch_movie_details(top_movie_ids)

    def fetch_movie_details(self, movie_ids: list[str]) -> list[dict]:
        """Fetch movie details by IDs."""
        resp = es.mget(index=self.movie_index, body={"ids": movie_ids})
        return [doc["_source"] for doc in resp["docs"] if doc["found"]]

    def recommend_top_rated(self, exclude: set[str], size: int = 10) -> list[dict]:
        """Recommend top-rated movies, excluding rated ones."""
        resp = es.search(index=self.movie_index, size=100, body={
            "query": {
                "range": {"average_rating": {"gte": 4.0}}
            },
            "sort": [{"average_rating": {"order": "desc"}}]
        })

        movies = []
        for hit in resp["hits"]["hits"]:
            if hit["_id"] not in exclude:
                movies.append(hit["_source"])
            if len(movies) >= size:
                break
        return movies
