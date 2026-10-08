"""add otp_code to users table

Revision ID: a1b2c3d4e5f6
Revises: 90f71aa8b235
Create Date: 2026-09-16 14:38:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '90f71aa8b235'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('otp_code', sa.String(length=10), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'otp_code')
