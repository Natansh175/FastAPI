from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from backend.db.db import Base
from backend.vo.login_vo import LoginVO


class UserVO(Base):
    __tablename__ = 'user_table'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_firstname = Column(String(20))
    user_lastname = Column(String(20))
    user_gender = Column(String(10))
    user_address = Column(String(255))
    created_date = Column(String(50))
    is_deleted = Column(Boolean, default=0)
    user_login_id = Column(Integer, ForeignKey(LoginVO.login_id,
                                               onupdate="CASCADE"), nullable=False)


    def serialize(self):
        return {
            'user_id': self.user_id,
            'user_firstname': self.user_firstname,
            'user_lastname': self.user_lastname,
            'user_gender': self.user_gender,
            'user_address': self.user_address,
            'created_date': self.created_date,
            'is_deleted': self.is_deleted,
            'user_login_id': self.user_login_id
        }
