from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from datetime import date

from .users import oauth2_scheme

from ..config import db
from ..utils.analytics import get_likes_analytics, get_user_activity

router = APIRouter(
    tags=['Analytics'],
    prefix="/analytics"
)

get_db = db.get_db


@router.get('/likes')
def read_likes_analytics(date_from: date, date_to: date, token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return get_likes_analytics(date_from, date_to, token, database)


@router.get('/user_activity')
def read_user_activity(token: str = Depends(oauth2_scheme)):
    return get_user_activity(token)
