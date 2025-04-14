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
```