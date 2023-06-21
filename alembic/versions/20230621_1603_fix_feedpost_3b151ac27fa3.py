"""fix feedpost

Revision ID: 3b151ac27fa3
Revises: cb0a6e2bcc35
Create Date: 2023-06-21 16:03:37.670856

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '3b151ac27fa3'
down_revision = 'cb0a6e2bcc35'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('feed_posts', sa.Column('id_feed', sa.BigInteger(), nullable=False))
    op.create_foreign_key('fk_feed_posts_feed_id', 'feed_posts', 'feeds', ['id_feed'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_feed_posts_feed_id', 'feed_posts', type_='foreignkey')
    op.drop_column('feed_posts', 'id_feed')
