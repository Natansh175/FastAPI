import bcrypt

from backend.vo.login_vo import LoginVO
from backend.dao.login_dao import LoginDAO
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum


class LoginServices:

    @staticmethod
    def validate_user(username, password):
        login_dao = LoginDAO()
        login_vo_list = login_dao.read_data_by_mail(username)
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
                    ResponseMessageEnum.NoUserFound,
                    False,
                    {}
                )

        if not login_vo_list:
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.NoUserFound,
                False,
                {}
            )
