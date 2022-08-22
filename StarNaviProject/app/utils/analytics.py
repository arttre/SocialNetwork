from fastapi import HTTPException, status

from sqlalchemy import Date, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import date, datetime

from .jwt import get_data_from_access_token
from .logs import find_user_last_login_log, find_user_last_service_request_log, \
    compose_user_service_request_log, write_user_logs


from ..config.db_tables import Likes, Users


def get_likes_analytics(date_from: date, date_to: date, token: str, database: Session):
    user_id = get_data_from_access_token(token)['id']
    write_user_logs(compose_user_service_request_log(user_id, datetime.utcnow()))

    try:
        list_of_likes_numbers_aggregated_by_day = database.\
            query(func.count(Likes.DateTime), Likes.DateTime.cast(Date)).\
            filter(Likes.DateTime > date_from, Likes.DateTime < date_to).\
            group_by(Likes.DateTime.cast(Date)).all()

        likes_analytics_aggregated_by_day = {}

        for row in list_of_likes_numbers_aggregated_by_day:
            likes_analytics_aggregated_by_day[row[1]] = row[0]

        return likes_analytics_aggregated_by_day

    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=Exception.args[1])


def get_user_activity(token: str):
    user_id = get_data_from_access_token(token)['id']

    user_activity = {
        'LastLoginDateTime': find_user_last_login_log(user_id),
        'LastRequestDateTime': find_user_last_service_request_log(user_id)
    }

    return user_activity
