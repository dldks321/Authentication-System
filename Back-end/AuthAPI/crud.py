from sqlalchemy.orm import Session

from models import User
from schemas import UserInfo


def get_user(database: Session, user_id: str):
    return database.query(User).filter(User.user_id == user_id).first()


def get_all_user(database: Session, init: int = 0, end: int = 100):
    return database.query(User).offset(init).limit(end).all()


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


def change_user_active(database: Session, user_id: str, active_info: bool = True):
    database.query(User).filter_by(user_id=user_id).update({"is_active": active_info})
    database.commit()
    return get_user(database, user_id)


def change_user_authority(database: Session, user_id: str, admin_info: bool = False):
    database.query(User).filter_by(user_id=user_id).update({"is_admin": admin_info})
    database.commit()
    return get_user(database, user_id)


def delete_user(database: Session, user_id: str):
    database.query(User).filter_by(user_id=user_id).delete()
    database.commit()
    return get_user(database, user_id)
