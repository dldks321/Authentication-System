from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, ExpiredSignatureError, jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, status

import models
from schemas import UserInfo, LoginUserInfo, RegisterUserInfo
from database import engine, get_database
from crud import create_user, get_user, get_all_user, change_user_active, change_user_authority, delete_user

SECRET_KEY = "b33b0d6db6ee8e0104fb095c5521f131c810165a2a016b8739d3b81a5411b2de"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
argon2_hash = PasswordHasher()


def create_access_token(payload_data: dict, expires_delta: Optional[timedelta] = None):
    token_body_data = payload_data.copy()
    if expires_delta:
        expire_time = datetime.utcnow() + expires_delta
    else:
        expire_time = datetime.utcnow() + timedelta(minutes=15)
    token_body_data.update({"exp": expire_time})
    encoded_jwt = jwt.encode(token_body_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/register")
async def register(inputted_user_info: RegisterUserInfo = Depends(), database: Session = Depends(get_database)):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User ID is already exist",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if get_user(database, inputted_user_info.user_id):
        raise auth_exception
    new_user = {
        "user_id": inputted_user_info.user_id,
        "encrypted_password": argon2_hash.hash(inputted_user_info.password),
        "email": inputted_user_info.email,
    }
    create_user(database, UserInfo(**new_user))
    return {"detail": "User successfully created"}


@app.post("/login")
async def login(inputted_user_info: LoginUserInfo = Depends(), database: Session = Depends(get_database)):
    user_info_in_db = get_user(database, inputted_user_info.user_id)
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect id or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not user_info_in_db:
        raise auth_exception
    try:
        argon2_hash.verify(user_info_in_db.encrypted_password, inputted_user_info.password)

        access_token = create_access_token(
            payload_data={"sub": user_info_in_db.user_id},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    except VerifyMismatchError:
        raise auth_exception
    return {"access_token": access_token, "token_type": "Bearer"}


@app.get("/verify")
async def verify_token(token: str, database: Session = Depends(get_database)):
    jwt_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is Invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        token_user_id = token_payload.get("sub")
        saved_user_info = get_user(database, token_user_id)
        if token_user_id is None or saved_user_info is None:
            raise jwt_exception
    except ExpiredSignatureError:
        jwt_exception.detail = "Token lifetime is expired"
        raise jwt_exception
    except JWTError:
        raise jwt_exception
    return {"detail": "Token validation successfully completed", "user": saved_user_info}


@app.get("/user/get_all")
async def get_all(init: int, end: int, database: Session = Depends(get_database)):
    return get_all_user(database, init, end)


@app.put("/user/change/active")
async def change_active(user_id: str, is_active: bool, database: Session = Depends(get_database)):
    return change_user_active(database, user_id, is_active)


@app.put("/user/change/admin")
async def change_admin(user_id: str, is_admin: bool, database: Session = Depends(get_database)):
    return change_user_authority(database, user_id, is_admin)


@app.delete("/user/delete")
async def delete(user_id: str, database: Session = Depends(get_database)):
    delete_user(database, user_id)
    return {"detail": "delete is complete"}
