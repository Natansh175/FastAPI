from datetime import datetime
import bcrypt

from backend.dto.register_dto import RegisterDTO
from backend.vo.login_vo import LoginVO
from backend.vo.user_vo import UserVO
from backend.dao.login_dao import LoginDAO
from backend.dao.register_dao import RegisterDAO
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.db.db import SessionLocal

# Apply logger once done.

db = SessionLocal()


class RegisterServices:

    @staticmethod
    def insert_user(user_info: RegisterDTO):
        try:
            login_vo = LoginVO()
            user_vo = UserVO()
            register_dao = RegisterDAO()
            login_dao = LoginDAO()


            user_vo_list = db.query(UserVO).filter(UserVO.user_email ==
                                                   user_info.email).all()

            if user_vo_list:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.UNAUTHORIZED,
                    ResponseMessageEnum.BadRequest,
                    False,
                    {}
                )

            name = user_info.first_name + " " + user_info.last_name

            salt = bcrypt.gensalt(rounds=12)
            password_hash = bcrypt.hashpw(user_info.password.encode("utf-8"),
                                          salt)
            login_vo.login_name = name
            login_vo.login_password = password_hash.decode("utf-8")
            login_vo.login_role = "user"
            login_vo.login_status = True
            login_dao.insert_login(login_vo)

            user_vo.user_firstname = user_info.first_name
            user_vo.user_lastname = user_info.last_name
            user_vo.user_email = user_info.email
            user_vo.user_gender = user_info.gender
            user_vo.user_address = user_info.address
            user_vo.created_date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_vo.user_login_id = login_vo.login_id

            register_dao.insert_user(user_vo)

            return ApplicationServices.application_response(
                HttpStatusCodeEnum.CREATED,
                ResponseMessageEnum.OK,
                True,
                {}
            )

        except Exception as exception:
            print(f"Insert user Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)
