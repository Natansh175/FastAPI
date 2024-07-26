from sqlalchemy import Boolean, Column, Integer, String

from backend.db.db import Base


class LoginVO(Base):
    __tablename__ = 'login_table'
    login_id = Column(Integer, primary_key=True, autoincrement=True)
    login_username = Column(String(200))
    login_password = Column(String(200))
    login_role = Column(String(20))
    login_status = Column(Boolean)
