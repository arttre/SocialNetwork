from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..config import db
from ..utils.users import register, login
from ..schemas.users import UserFullInfo


router = APIRouter(
    tags=['Users'],
    prefix="/user"
)

get_db = db.get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post('/signup')
def user_registration(user: UserFullInfo, database: Session = Depends(get_db)):
    return register(user, database)


@router.post('/login')
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_db)):
    return login(form_data, database)
