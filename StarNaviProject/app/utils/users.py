from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import datetime

from .jwt import create_access_token
from .hashing import verify_password, hash_password
from .logs import write_user_logs, compose_user_login_log

from ..config.db_tables import Users
from ..schemas.users import UserFullInfo


def register(user: UserFullInfo, database: Session):
    try:
        new_user = Users(Email=user.email, FirstName=user.first_name,
                         LastName=user.last_name, Password=hash_password(user.password))

        database.add(new_user)
        database.commit()
        database.refresh(new_user)

    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=err.orig.args[1])

    return new_user


def login(form_data: OAuth2PasswordRequestForm, database: Session):
    try:
        current_user_info = database.query(Users).filter(Users.Email == form_data.username).first()

        if not current_user_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Invalid Credentials")
        if not verify_password(current_user_info.Password, form_data.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Incorrect password")

        jwt_token = create_access_token(data={
            'id': current_user_info.UserID
        })

        write_user_logs(compose_user_login_log(current_user_info.UserID, datetime.utcnow()))

    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with credentials')

    return {'access_token': jwt_token, 'token_type': 'bearer'}
