import typing as tp

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from db import engine, execute_all_users, get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db_session = get_session(engine)


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def decode_token(token):
    users_db = execute_all_users(db_session)
    user = get_user(users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        return None
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        return None
    return current_user
