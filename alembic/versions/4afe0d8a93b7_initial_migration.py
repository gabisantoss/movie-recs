"""Initial migration

Revision ID: 4afe0d8a93b7
Revises: 
Create Date: 2025-04-13 16:17:33.764499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '4afe0d8a93b7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'genres',
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('name')
    )

    op.create_table(
        'actors',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(), nullable=False)
    )

    op.create_table(
        'directors',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(), nullable=False)
    )

    op.create_table(
        'movies',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('average_rating', sa.Float(), nullable=True),
        sa.Column('director_id', sa.UUID(), sa.ForeignKey(
            'directors.id'), nullable=True)
    )

    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(), nullable=False, unique=True)
    )

    op.create_table(
        'user_movies',
        sa.Column('user_id', sa.UUID(), sa.ForeignKey(
            'users.id'), primary_key=True),
        sa.Column('movie_id', sa.UUID(), sa.ForeignKey(
            'movies.id'), primary_key=True),
        sa.Column('rating', sa.Float(), nullable=False)
    )

    op.create_table(
        'movie_actors',
        sa.Column('movie_id', sa.UUID(), sa.ForeignKey(
            'movies.id'), primary_key=True),
        sa.Column('actor_id', sa.UUID(), sa.ForeignKey(
            'actors.id'), primary_key=True)
    )

    op.create_table(
        'movie_genres',
        sa.Column('movie_id', sa.UUID(), sa.ForeignKey(
            'movies.id'), primary_key=True),
        sa.Column('genre', sa.String(), sa.ForeignKey(
            'genres.name'), primary_key=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('movie_genres')
    op.drop_table('movie_actors')
    op.drop_table('user_movies')
    op.drop_table('users')
    op.drop_table('movies')
    op.drop_table('directors')
    op.drop_table('actors')
    op.drop_table('genres')
