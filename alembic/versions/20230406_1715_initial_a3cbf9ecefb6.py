"""initial

Revision ID: a3cbf9ecefb6
Revises: 
Create Date: 2023-04-06 17:15:49.979721

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a3cbf9ecefb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('users')
