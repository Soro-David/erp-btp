"""add company_name and company_logo to users

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-09-20 19:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('company_name', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('company_logo', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'company_logo')
    op.drop_column('users', 'company_name')
