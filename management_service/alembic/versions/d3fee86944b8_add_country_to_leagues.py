"""Add country to leagues

Revision ID: d3fee86944b8
Revises: 
Create Date: 2025-02-11 17:17:38.766831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3fee86944b8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('leagues', sa.Column('country', sa.String(), nullable=True))


def downgrade():
    op.drop_column('leagues', 'country')