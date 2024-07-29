from datetime import datetime, timedelta
import bcrypt
import jwt
from fastapi import Response
from functools import wraps

from backend.dto.register_dto import RegisterDTO
from backend.vo.login_vo import LoginVO
from backend.vo.user_vo import UserVO
from backend.dao.authentication_dao import AuthenticationDAO
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.enum.authentication_enum import AuthenticationEnum


def refresh_token(request, fn):
    try:
        authentication_dao = AuthenticationDAO()
        # refreshtoken = request.COOKIES.get('refreshtoken')
        cookie = request.headers.get('cookie')
        refreshtoken = None
        if cookie:
            cookies = cookie.split('; ')
            for c in cookies:
                if c.startswith('refreshtoken='):
                    refreshtoken = c[len('refreshtoken='):]
                    break
        if refreshtoken is not None:
            data = jwt.decode(refreshtoken, algorithms=["HS256"],
                              options={"verify_signature": False})

            login_vo_list = authentication_dao.read_user_immutable(
                data['upload_id'])

            response = fn(request)
            response.set_cookie(
                AuthenticationEnum.ACCESSTOKEN.value,
                value=jwt.encode({
                    'public_id': login_vo_list[0].login_username,
                    'role': login_vo_list[0].login_role,
                    'exp': datetime.utcnow() + timedelta(
                        minutes=int(AuthenticationEnum.ACCESS_TOKEN_EXP.value))
                },
                    AuthenticationEnum.HASH_ALGORITHM),
                max_age=int(AuthenticationEnum.ACCESS_TOKEN_MAX_AGE.value)
            )

            refresh = jwt.encode({
                'public_id': login_vo_list[0].login_username,
                'exp': datetime.utcnow() + timedelta(
                    hours=int(AuthenticationEnum.REFRESH_TOKEN_EXP.value))
            },
                AuthenticationEnum.HASH_ALGORITHM)
            print("NEW TOKEN CREATED!!")
            response.set_cookie(
                AuthenticationEnum.REFRESHTOKEN.value,
                value=refresh,
                max_age=int(AuthenticationEnum.REFRESH_TOKEN_MAX_AGE.value)
            )
            return response

        else:
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.UNAUTHORIZED.value,
                ResponseMessageEnum.UserNotFound,
                False,
                {}
            )

    except Exception as exception:
        print(f"Refresh Token function exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


def login_required(role):
    def inner(fn):
        @wraps(fn)
        async def decorator(*args, **kwargs):
            request = kwargs.get('request')
            response = kwargs.get('response')
            try:
                cookie = request.headers.get('cookie')
                accesstoken = None
                if cookie:
                    cookies = cookie.split('; ')
                    for c in cookies:
                        if c.startswith('accesstoken='):
                            accesstoken = c[len('accesstoken='):]
                            break
                if accesstoken is None:
                    return await refresh_token(request, fn)

                else:
                    authentication_dao = AuthenticationDAO()
                    data = jwt.decode(accesstoken, algorithms=["HS256"],
                                      options={"verify_signature": False})
                    login_vo_list = authentication_dao.read_user_immutable(
                        data.get('public_id'))
                    if login_vo_list is not None:
                        if login_vo_list.login_role == role and login_vo_list.login_status:
                            return await fn(*args, **kwargs)
                        else:
                            response.status_code = HttpStatusCodeEnum.UNAUTHORIZED
                            return ResponseMessageEnum.Unauthorized.value
                    else:
                        response.status_code = HttpStatusCodeEnum.UNAUTHORIZED
                        return ApplicationServices.application_response(
                            HttpStatusCodeEnum.UNAUTHORIZED,
                            ResponseMessageEnum.UserNotFound,
                            False,
                            {}
                        )
            except Exception as exception:
                print(f"Login Required Exception: {exception}")
                return ApplicationServices.handle_exception(exception, True)

        return decorator

    return inner


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

            user_vo_list = authentication_dao.read_user_immutable(
                user_info.email)

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
            user_vo.created_date = datetime.strftime(datetime.now(),
                                                     '%Y-%m-%d %H:%M:%S')
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
    def app_login(email, password, response: Response):
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
            login_role = login_vo_list.login_role
            if bcrypt.checkpw(user_password, login_hashed_password):

                if login_role == 'admin':
                    response.set_cookie(
                        AuthenticationEnum.ACCESSTOKEN.value,
                        value=jwt.encode({
                            'public_id': email,
                            'role': login_role,
                            'exp': datetime.utcnow() + timedelta(
                                   minutes=int(AuthenticationEnum.ACCESS_TOKEN_EXP.value))
                        },
                            AuthenticationEnum.HASH_ALGORITHM),
                        max_age=int(AuthenticationEnum.ACCESS_TOKEN_MAX_AGE.value)
                    )

                    refresh = jwt.encode({
                        'public_id': email,
                        'exp': datetime.utcnow() + timedelta(
                            hours=int(AuthenticationEnum.REFRESH_TOKEN_EXP.value))
                        },
                        AuthenticationEnum.HASH_ALGORITHM)
                    response.set_cookie(
                        AuthenticationEnum.REFRESHTOKEN.value,
                        value=refresh,
                        max_age=int(AuthenticationEnum.REFRESH_TOKEN_MAX_AGE.value)
                    )

                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK,
                        ResponseMessageEnum.LoggedIn,
                        True,
                        {}
                    )

                elif login_role == 'user':
                    response.set_cookie(
                        AuthenticationEnum.ACCESSTOKEN.value,
                        value=jwt.encode({
                            'public_id': email,
                            'role': login_role,
                            'exp': datetime.utcnow() + timedelta(
                                   minutes=int(AuthenticationEnum.ACCESS_TOKEN_EXP.value))
                        },
                            AuthenticationEnum.HASH_ALGORITHM),
                        max_age=int(AuthenticationEnum.ACCESS_TOKEN_MAX_AGE.value)
                    )

                    refresh = jwt.encode({
                        'public_id': email,
                        'exp': datetime.utcnow() + timedelta(
                            hours=int(AuthenticationEnum.REFRESH_TOKEN_EXP.value))
                        },
                        AuthenticationEnum.HASH_ALGORITHM)
                    response.set_cookie(
                        AuthenticationEnum.REFRESHTOKEN.value,
                        value=refresh,
                        max_age=int(AuthenticationEnum.REFRESH_TOKEN_MAX_AGE.value)
                    )

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
