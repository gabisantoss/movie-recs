from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from src.infrastructure.database.models.director import Director


class DirectorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, director_id: UUID) -> Director:
        return self.db.get(director_id)
