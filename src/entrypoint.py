import subprocess
import uvicorn


def run_migrations():
    print("🛠 Running Alembic migrations...")
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    print("✅ Migrations applied")


def start_api():
    print("🚀 Starting FastAPI app...")
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_migrations()
    start_api()
