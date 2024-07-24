from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from backend.db.db import Base
from backend.vo.login_vo import LoginVO


class UserVO(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_firstname = Column(String(200))
    user_lastname = Column(String(200))
    user_email = Column(String(50))
    user_gender = Column(String(10))
    user_address = Column(String(500))
    is_deleted = Column(Boolean, default=False)
    created_date = Column(String(50))
    user_login_id = Column(Integer, ForeignKey(LoginVO.login_id,
                                               ONUPDATE="CASCADE"), nullable=False)
