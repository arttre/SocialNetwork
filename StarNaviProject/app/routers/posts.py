from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from .users import oauth2_scheme

from ..config import db
from ..schemas.posts import Post
from ..utils.posts import get_all_posts, get_specific_user_posts, \
    create_post, like_specific_post, unlike_specific_post

router = APIRouter(
    tags=['Posts'],
    prefix="/post"
)

get_db = db.get_db


@router.get('/get_all')
def read_all_posts(database: Session = Depends(get_db)):
    return get_all_posts(database)


@router.get('/get_my')
def read_specific_user_posts(token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return get_specific_user_posts(token, database)


@router.post('/create')
def create(post_info: Post, token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return create_post(post_info, token, database)


@router.post('/like/{post_id}')
def like_post(post_id: int, token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return like_specific_post(post_id, token, database)


@router.post('/unlike/{post_id}')  # @router.delete()?
def like_post(post_id: int, token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return unlike_specific_post(post_id, token, database)
