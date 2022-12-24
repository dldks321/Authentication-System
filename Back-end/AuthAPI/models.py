from sqlalchemy import Column, Integer, String, CHAR, Boolean
from database import Base


class User(Base):
    __tablename__ = "UserInfo"

    user_id = Column(String(40), primary_key=True, index=True)
    encrypted_password = Column(String(100))
    email = Column(String(40))
    is_active = Column(Boolean)
    is_admin = Column(Boolean)
