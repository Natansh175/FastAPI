from datetime import datetime
import bcrypt

from backend.dto.register_dto import RegisterDTO
from backend.vo.login_vo import LoginVO
from backend.vo.user_vo import UserVO
from backend.dao.authentication_dao import AuthenticationDAO
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum


class AuthenticationServices:

    @staticmethod
    def insert_user(user_info: RegisterDTO):
        try:
            login_vo = LoginVO()
            user_vo = UserVO()
            authentication_dao = AuthenticationDAO()

            for key, value in user_info:
                if value == "":
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.UNPROCESSABLE_ENTITY,
                        ResponseMessageEnum.NotValidInput,
                        False,
                        {}
                    )

            user_vo_list = authentication_dao.read_user_immutable(user_info.email)

            if user_vo_list:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.CONFLICT,
                    ResponseMessageEnum.UserExists,
                    False,
                    {}
                )

            salt = bcrypt.gensalt(rounds=12)
            password_hash = bcrypt.hashpw(user_info.password.encode("utf-8"),
                                          salt)

            login_vo.login_username = user_info.email
            login_vo.login_password = password_hash.decode("utf-8")
            login_vo.login_role = "user"
            login_vo.login_status = True
            authentication_dao.insert_login(login_vo)

            user_vo.user_firstname = user_info.first_name
            user_vo.user_lastname = user_info.last_name
            user_vo.user_gender = user_info.gender
            user_vo.user_address = user_info.address
            user_vo.created_date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_vo.user_login_id = login_vo.login_id

            authentication_dao.insert_user(user_vo)

            return ApplicationServices.application_response(
                HttpStatusCodeEnum.CREATED,
                ResponseMessageEnum.UserCreatedSuccessfully,
                True,
                {}
            )

        except Exception as exception:
            print(f"Insert user Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def validate_user(email, password):
        authentication_dao = AuthenticationDAO()

        login_vo_list = authentication_dao.read_user_immutable(email)

        user_password = password.encode('utf-8')

        if login_vo_list:
            if not login_vo_list.login_status:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.UNAUTHORIZED,
                    ResponseMessageEnum.UserBlocked,
                    False,
                    {}
                )

            login_hashed_password = login_vo_list.login_password.encode('utf-8')
            if bcrypt.checkpw(user_password, login_hashed_password):

                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.OK,
                    ResponseMessageEnum.LoggedIn,
                    True,
                    {}
                )

            else:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.IncorrectPassword,
                    False,
                    {}
                )

        if login_vo_list is None:
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.UserNotFound,
                False,
                {}
            )
