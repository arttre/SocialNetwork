from sqlalchemy import Column, String, ForeignKey, BigInteger, DateTime, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from datetime import datetime

from .db import Base, engine


class Users(Base):
    __tablename__ = 'Users'

    UserID = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Email = Column(String(255), unique=True, nullable=False)
    FirstName = Column(String(255), nullable=False)
    LastName = Column(String(255), nullable=False)
    Password = Column(String(255), nullable=False)

    posts = relationship('Posts', back_populates='creator', cascade='all, delete', passive_deletes=True)
    likes = relationship('Likes', back_populates='like_user', cascade='all, delete', passive_deletes=True)


class Posts(Base):
    __tablename__ = 'Posts'

    PostID = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Title = Column(String(255), nullable=False)
    Body = Column(String(255), nullable=False)
    Creator = Column(BigInteger, ForeignKey('Users.UserID', ondelete='CASCADE'), nullable=False)
    CreationDateTime = Column(DateTime, nullable=False)
    LikesNumber = Column(BigInteger, nullable=False)

    creator = relationship('Users', back_populates='posts')
    likes = relationship('Likes', back_populates='like_post', cascade='all, delete', passive_deletes=True)


class Likes(Base):
    __tablename__ = 'Likes'

    LikeID = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    User = Column(BigInteger, ForeignKey('Users.UserID', ondelete='CASCADE'))
    Post = Column(BigInteger, ForeignKey('Posts.PostID', ondelete='CASCADE'))
    DateTime = Column(DateTime, nullable=False)

    like_user = relationship('Users', back_populates='likes')
    like_post = relationship('Posts', back_populates='likes')

    UniqueConstraint('User', 'Post')


Base.metadata.create_all(engine)
