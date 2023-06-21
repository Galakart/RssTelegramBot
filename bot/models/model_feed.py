from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Text

from .base import Base


class Feed(Base):
    __tablename__ = "feeds"
    __table_args__ = {"comment": "RSS ленты"}

    id = Column(BigInteger, primary_key=True)
    link = Column(Text, nullable=False, unique=True)
    title = Column(Text, nullable=False)
    id_author = Column(BigInteger, ForeignKey('users.id'), comment='Юзер, который первый раз добавил эту ленту')
    datetime_last_update = Column(DateTime)


class FeedPost(Base):
    __tablename__ = "feed_posts"
    __table_args__ = {"comment": "Посты в ленте"}

    id = Column(BigInteger, primary_key=True)
    id_feed = Column(BigInteger, ForeignKey('feeds.id'), nullable=False)
    title = Column(Text)
    description = Column(Text, nullable=False)
    link = Column(Text)
    datetime_published = Column(DateTime)


class UserFeed(Base):
    __tablename__ = "user_feeds"
    __table_args__ = {"comment": "Ленты на которые подписан юзер"}

    id_user = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    id_feed = Column(BigInteger, ForeignKey('feeds.id'), primary_key=True)
    id_last_post = Column(BigInteger, ForeignKey('feed_posts.id'))
