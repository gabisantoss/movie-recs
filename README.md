# 🎬 Movie Recs API
A movie recommendation API powered by Elasticsearch. It delivers personalized recommendations based on user behavior and fallback strategies for new users.

## 🚀 Getting Started

### 🔧 Running with Docker

1. Clone the repository:
```bash
git clone https://github.com/gabisantoss/movie-recs
cd movie-recs
```

2. Create environment variables
```bash
cp .env.example .env
```

3. Build and start the containers

```bash
docker-compose up --build
```

🎉 The API will be available at http://localhost:8000

### 🔧 Running Locally with Python

1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
.\venv\Scripts\activate         # Windows
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Configure environment: Edit .env with your local Elasticsearch and Postgres connection details.

4. Run the application

```
python -m src.entrypoint
```

## 📡 API Endpoints

| Method |      Route    | Return        |
| :-------:| :-------------: |:-------------:|
|   **GET**  | /movies/      | Retrieve all movies.     |
|   **GET**  | /movies/recommendations | Retrieve user movie recommendations. |

## 🧠 Recommendation Algorithm
This application uses a hybrid recommendation strategy based on Elasticsearch queries, designed for scalability and simplicity without external ML models.

### 🔁 Collaborative Filtering (User-Based)
The main recommendation engine is based on user-based collaborative filtering, which works as follows:

1. Fetches movies the current user has rated.
2. Identifies users who rated the same movies (excluding the current user).
3. Gathers movies highly rated (≥ 4.0) by those similar users, filters out already seen content, and ranks them by frequency.
4. Retrieves full movie data for the top recommendations using Elasticsearch’s mget.

### 📉 Cold Start Fallback (Top Rated)
If the user has no rating history or no similar users are found, the system falls back to a content-based approach:
1. Recommends movies with a high average_rating, sorted in descending order.
2. Filters out any previously rated movies.

## 🌱 Automatic Database Seeder
To make development and testing easier, this project includes an automatic seeder that populates both the PostgreSQL database and Elasticsearch with dummy data on its entrypoint.

### 🎯 Purpose
- The seeder generates:
    - A collection of movies with randomly assigned genres, directors, actors, and average ratings.
    - Several users, each with randomly rated movies.
    - Full synchronization with Elasticsearch, indexing all movies and ratings.

This dummy data enables immediate testing of the recommendation algorithm without needing to manually insert records.

## 📂 Project Structure

```
src/
├── api/
│   └── routes/
│       └── movies.py
├── domain/
│   └── entities.py
├── infrastructure/
│   ├── database/
│   │   ├── models/
│   │   │   ├── actor.py
│   │   │   ├── director.py
│   │   │   ├── genre.py
│   │   │   ├── movie.py
│   │   │   ├── user_movie.py
│   │   │   └── user.py
│   │   ├── base.py
│   │   └── session.py
│   └── elastic/
│       └── client.py
├── repositories/           
│   └── movie_repository.py
├── services/           
│   └── recommend_service.py
├── utils/           
│   └── seed.py
└── entrypoint.py
```

## 🧪 Example .env
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_USER=elastic
ELASTICSEARCH_PASSWORD=changeme
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```