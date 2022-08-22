from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import datetime

from .jwt import get_data_from_access_token
from .logs import write_user_logs, compose_user_service_request_log

from ..config.db_tables import Posts, Likes
from ..schemas.posts import Post


def get_all_posts(database: Session):
    return database.query(Posts).all()


def get_specific_user_posts(token: str, database: Session):
    user_id = get_data_from_access_token(token)['id']
    write_user_logs(compose_user_service_request_log(user_id, datetime.utcnow()))

    return database.query(Posts).filter(Posts.Creator == user_id).all()


def create_post(post_info: Post, token: str, database: Session):
    user_id = get_data_from_access_token(token)['id']
    write_user_logs(compose_user_service_request_log(user_id, datetime.utcnow()))

    try:
        new_post = Posts(Title=post_info.Title, Body=post_info.Body, Creator=user_id,
                         CreationDateTime=datetime.utcnow(), LikesNumber=0)

        database.add(new_post)
        database.commit()
        database.refresh(new_post)

    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=err.orig.args[1])

    return new_post


def like_specific_post(post_id: int, token: str, database: Session):
    user_id = get_data_from_access_token(token)['id']
    write_user_logs(compose_user_service_request_log(user_id, datetime.utcnow()))

    try:
        if database.query(Likes).filter(Likes.User == user_id, Likes.Post == post_id).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="You can make only one like")

        database.query(Posts).filter(Posts.PostID == post_id).update({'LikesNumber': Posts.LikesNumber + 1})
        database.commit()

        new_like = Likes(User=user_id, Post=post_id, DateTime=datetime.utcnow())

        database.add(new_like)
        database.commit()
        database.refresh(new_like)

    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=err.orig.args[1])

    return new_like


def unlike_specific_post(post_id: int, token: str, database: Session):
    user_id = get_data_from_access_token(token)['id']
    write_user_logs(compose_user_service_request_log(user_id, datetime.utcnow()))

    like_query = database.query(Likes).filter(Likes.User == user_id, Likes.Post == post_id)

    try:
        if not like_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="You can not unlike this post")

        database.query(Posts).filter(Posts.PostID == post_id).update({'LikesNumber': Posts.LikesNumber - 1})
        database.commit()

        removed_like = like_query.first()

        like_query.delete()
        database.commit()

    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=err.orig.args[1])

    return removed_like
