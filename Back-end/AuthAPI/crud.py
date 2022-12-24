from sqlalchemy.orm import Session

from models import User
from schemas import UserInfo


def get_user(database: Session, user_id: str):
    return database.query(User).filter(User.user_id == user_id).first()


def create_user(database: Session, user: UserInfo):
    database_user = User(user_id=user.user_id,
                         encrypted_password=user.encrypted_password,
                         email=user.email,
                         is_active=user.is_active,
                         is_admin=user.is_admin)
    database.add(database_user)
    database.commit()
    database.refresh(database_user)
    return database_user
