"""Add is_flagged and threat_score to logs

Revision ID: e398a9ceaa51
Revises: 
Create Date: 2025-07-11 04:17:59.099365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e398a9ceaa51'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('logs', sa.Column('is_flagged', sa.Boolean(), server_default=sa.text('false')))
    op.add_column('logs', sa.Column('threat_score', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('logs', 'threat_score')
    op.drop_column('logs', 'is_flagged')