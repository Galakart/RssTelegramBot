"""users and feeds

Revision ID: cb0a6e2bcc35
Revises: a3cbf9ecefb6
Create Date: 2023-06-19 11:11:58.182700

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'cb0a6e2bcc35'
down_revision = 'a3cbf9ecefb6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('feed_posts',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('title', sa.Text(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.Column('link', sa.Text(), nullable=True),
                    sa.Column('datetime_published', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Посты в ленте'
                    )
    op.create_table('feeds',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('link', sa.Text(), nullable=False),
                    sa.Column('title', sa.Text(), nullable=False),
                    sa.Column('id_author', sa.BigInteger(), nullable=True, comment='Юзер, который первый раз добавил эту ленту'),
                    sa.Column('datetime_last_update', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['id_author'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('link'),
                    comment='RSS ленты'
                    )
    op.create_table('user_feeds',
                    sa.Column('id_user', sa.BigInteger(), nullable=False),
                    sa.Column('id_feed', sa.BigInteger(), nullable=False),
                    sa.Column('id_last_post', sa.BigInteger(), nullable=True),
                    sa.ForeignKeyConstraint(['id_feed'], ['feeds.id'], ),
                    sa.ForeignKeyConstraint(['id_last_post'], ['feed_posts.id'], ),
                    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id_user', 'id_feed'),
                    comment='Ленты на которые подписан юзер'
                    )
    op.add_column('users', sa.Column('nick', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('active', sa.Boolean(), nullable=False))
    op.create_table_comment(
        'users',
        'Юзеры',
        existing_comment=None,
        schema=None
    )


def downgrade() -> None:
    op.drop_table_comment(
        'users',
        existing_comment='Юзеры',
        schema=None
    )
    op.drop_column('users', 'active')
    op.drop_column('users', 'nick')
    op.drop_table('user_feeds')
    op.drop_table('feeds')
    op.drop_table('feed_posts')
