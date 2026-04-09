"""add user profile fields

Revision ID: 7d2a9f0c1b3e
Revises: 5c1bc2b86211
Create Date: 2026-04-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7d2a9f0c1b3e"
down_revision: Union[str, Sequence[str], None] = "5c1bc2b86211"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if not inspector.has_table("users"):
        return
    existing = {c["name"] for c in inspector.get_columns("users")}
    if "display_name" not in existing:
        op.add_column("users", sa.Column("display_name", sa.String(length=100), nullable=True))
    if "bio" not in existing:
        op.add_column("users", sa.Column("bio", sa.Text(), nullable=True))
    if "avatar_url" not in existing:
        op.add_column("users", sa.Column("avatar_url", sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "avatar_url")
    op.drop_column("users", "bio")
    op.drop_column("users", "display_name")
