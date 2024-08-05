from sqlalchemy import Boolean, Column, Integer, String

from backend.db.db import Base


class LoginVO(Base):
    __tablename__ = 'login_table'
    login_id = Column(Integer, primary_key=True, autoincrement=True)
    login_username = Column(String(100))
    login_password = Column(String(100))
    login_role = Column(String(20))
    login_status = Column(Boolean)

    def serialize(self):
        return {
            'login_id': self.login_id,
            'login_username': self.login_username,
            'login_password': self.login_password,
            'login_role': self.login_role,
            'login_status': self.login_status
        }
