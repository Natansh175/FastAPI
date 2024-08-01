import logging
from datetime import datetime, timedelta
import bcrypt
import jwt
from fastapi import Response
from functools import wraps

from backend.vo.login_vo import LoginVO
from backend.vo.user_vo import UserVO
from backend.dao.authentication_dao import AuthenticationDAO
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.enum.authentication_enum import AuthenticationEnum


# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler for all logs
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler for error logs
file_handler = logging.FileHandler('backend/logs/authentication_services.log')
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


async def refresh_token(fn, role, **kwargs):
    response = kwargs.get('response')
    request = kwargs.get('request')
    logger.info("Refreshing tokens.")
    try:
        authentication_dao = AuthenticationDAO()
        refreshtoken = request.cookies.get(AuthenticationEnum.REFRESHTOKEN.value)
        if refreshtoken is not None:
            data = jwt.decode(refreshtoken, AuthenticationEnum.SECRET_KEY,
                              algorithms=["HS256"])

            login_vo_list = authentication_dao.read_user_by_email(data['public_id'])

            response.set_cookie(
                AuthenticationEnum.ACCESSTOKEN.value,
                value=jwt.encode({
                    'public_id': login_vo_list.login_username,
                    'role': login_vo_list.login_role,
                    'exp': datetime.utcnow() + timedelta(minutes=int(AuthenticationEnum.ACCESS_TOKEN_EXP.value))
                }, AuthenticationEnum.SECRET_KEY,
                    AuthenticationEnum.HASH_ALGORITHM),
                max_age=int(AuthenticationEnum.ACCESS_TOKEN_MAX_AGE.value)
            )

            refresh = jwt.encode({
                'public_id': login_vo_list.login_username,
                'exp': datetime.utcnow() + timedelta(hours=int(AuthenticationEnum.REFRESH_TOKEN_EXP.value))
            }, AuthenticationEnum.SECRET_KEY,  AuthenticationEnum.HASH_ALGORITHM)
            logger.info("New tokens created.")
            response.set_cookie(
                AuthenticationEnum.REFRESHTOKEN.value,
                value=refresh,
                max_age=int(AuthenticationEnum.REFRESH_TOKEN_MAX_AGE.value)
            )

            if login_vo_list.login_role in role and \
                    login_vo_list.login_status:
                return await fn(**kwargs)
            else:
                logger.info(f"{login_vo_list.login_username} is unauthorized for {fn}")
                response.status_code = HttpStatusCodeEnum.UNAUTHORIZED.value
                return ResponseMessageEnum.Unauthorized

        else:
            logger.warning("Refresh token not found")
            response.status_code = HttpStatusCodeEnum.UNAUTHORIZED
            return ResponseMessageEnum.LogInAgain

    except Exception as exception:
        logger.error(f"Refresh Token function exception: {exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)


def login_required(role):
    def inner(fn):
        @wraps(fn)
        async def decorator(**kwargs):
            response = kwargs.get('response')
            request = kwargs.get('request')
            try:
                accesstoken = request.cookies.get(AuthenticationEnum.ACCESSTOKEN.value)

                if accesstoken is None:
                    return await refresh_token(fn, role, **kwargs)
                else:
                    authentication_dao = AuthenticationDAO()
                    try:
                        data = jwt.decode(accesstoken, AuthenticationEnum.SECRET_KEY, algorithms=["HS256"])

                    except jwt.exceptions.InvalidSignatureError:
                        return ResponseMessageEnum.Unauthorized

                    except jwt.exceptions.ExpiredSignatureError:
                        return await refresh_token(fn, role, **kwargs)

                    login_vo_list = authentication_dao.read_user_by_email(data.get('public_id'))
                    if login_vo_list is not None:
                        if login_vo_list.login_role in role and \
                                login_vo_list.login_status:
                            return await fn(**kwargs)
                        else:
                            logger.info(f"{data.get('public_id')} with role "
                                        f"{data.get('role')} is not "
                                        f"authorized for {fn}")
                            response.status_code = HttpStatusCodeEnum.UNAUTHORIZED
                            return ResponseMessageEnum.Unauthorized.value
                    else:
                        response.status_code = HttpStatusCodeEnum.UNAUTHORIZED
                        return ResponseMessageEnum.UserNotFound

            except Exception as exception:
                logger.error(f"Login Required Exception: {exception}", exc_info=True)
                return ApplicationServices.handle_exception(exception, True)

        return decorator

    return inner


class AuthenticationServices:

    @staticmethod
    def insert_user(user_info):
        logger.info("Inserting a new user.")
        try:
            login_vo = LoginVO()
            user_vo = UserVO()
            authentication_dao = AuthenticationDAO()

            user_vo_list = authentication_dao.read_user_by_email(user_info.email)

            if user_vo_list:
                logger.warning(f"User with email {user_info.email} already "
                               f"exists.")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.CONFLICT,
                    ResponseMessageEnum.UserExists,
                    False,
                    {}
                )

            salt = bcrypt.gensalt(rounds=12)
            password_hash = bcrypt.hashpw(user_info.password.encode("utf-8"), salt)

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

            logger.info(f"User '{user_info.email}' inserted successfully.")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.CREATED,
                ResponseMessageEnum.UserCreatedSuccessfully,
                True,
                {}
            )
        except Exception as exception:
            logger.error(f"Insert user Services Exception: {exception}", exc_info=True)
            return ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def app_login(email, password, response: Response):
        logger.info(f"Login attempt with email: {email}.")
        authentication_dao = AuthenticationDAO()

        login_vo_list = authentication_dao.read_user_by_email(email)

        user_password = password.encode('utf-8')

        if login_vo_list:
            if not login_vo_list.login_status:
                logger.warning(f"User with email {email} is blocked.")
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
                            'exp': datetime.utcnow() + timedelta(minutes=int(AuthenticationEnum.ACCESS_TOKEN_EXP.value))
                        }, AuthenticationEnum.SECRET_KEY,
                            AuthenticationEnum.HASH_ALGORITHM),
                        max_age=int(AuthenticationEnum.ACCESS_TOKEN_MAX_AGE.value)
                    )

                    refresh = jwt.encode({
                        'public_id': email,
                        'exp': datetime.utcnow() + timedelta(hours=int(AuthenticationEnum.REFRESH_TOKEN_EXP.value))
                    }, AuthenticationEnum.SECRET_KEY, AuthenticationEnum.HASH_ALGORITHM)
                    response.set_cookie(
                        AuthenticationEnum.REFRESHTOKEN.value,
                        value=refresh,
                        max_age=int(AuthenticationEnum.REFRESH_TOKEN_MAX_AGE.value)
                    )

                    logger.info(f"Admin user '{email}' logged in "
                                f"successfully as {login_role}.")
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
                            'exp': datetime.utcnow() + timedelta(minutes=int(AuthenticationEnum.ACCESS_TOKEN_EXP.value))
                        }, AuthenticationEnum.SECRET_KEY, AuthenticationEnum.HASH_ALGORITHM),
                        max_age=int(AuthenticationEnum.ACCESS_TOKEN_MAX_AGE.value)
                    )

                    refresh = jwt.encode({
                        'public_id': email,
                        'exp': datetime.utcnow() + timedelta(hours=int(AuthenticationEnum.REFRESH_TOKEN_EXP.value))
                    }, AuthenticationEnum.SECRET_KEY, AuthenticationEnum.HASH_ALGORITHM)
                    response.set_cookie(
                        AuthenticationEnum.REFRESHTOKEN.value,
                        value=refresh,
                        max_age=int(AuthenticationEnum.REFRESH_TOKEN_MAX_AGE.value)
                    )

                    logger.info(f"User '{email}' logged in successfully as "
                                f"{login_role}.")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK,
                        ResponseMessageEnum.LoggedIn,
                        True,
                        {}
                    )

                elif login_role == 'seller':
                    response.set_cookie(
                        AuthenticationEnum.ACCESSTOKEN.value,
                        value=jwt.encode({
                            'public_id': email,
                            'role': login_role,
                            'exp': datetime.utcnow() + timedelta(minutes=int(AuthenticationEnum.ACCESS_TOKEN_EXP.value))
                        }, AuthenticationEnum.SECRET_KEY, AuthenticationEnum.HASH_ALGORITHM),
                        max_age=int(AuthenticationEnum.ACCESS_TOKEN_MAX_AGE.value)
                    )

                    refresh = jwt.encode({
                        'public_id': email,
                        'exp': datetime.utcnow() + timedelta(hours=int(AuthenticationEnum.REFRESH_TOKEN_EXP.value))
                    }, AuthenticationEnum.SECRET_KEY, AuthenticationEnum.HASH_ALGORITHM)
                    response.set_cookie(
                        AuthenticationEnum.REFRESHTOKEN.value,
                        value=refresh,
                        max_age=int(AuthenticationEnum.REFRESH_TOKEN_MAX_AGE.value)
                    )

                    logger.info(f"User '{email}' logged in successfully as "
                                f"{login_role}.")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK,
                        ResponseMessageEnum.LoggedIn,
                        True,
                        {}
                    )

            else:
                logger.warning(f"Incorrect password for email {email}")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.IncorrectPassword,
                    False,
                    {}
                )

        logger.warning(f"User with email {email} not found")
        return ApplicationServices.application_response(
            HttpStatusCodeEnum.NOT_FOUND,
            ResponseMessageEnum.UserNotFound,
            False,
            {}
        )

    @staticmethod
    def app_logout(user_email, response: Response):
        logger.info(f"{user_email} attempted for logout.")
        response.delete_cookie(AuthenticationEnum.ACCESSTOKEN.value)
        response.delete_cookie(AuthenticationEnum.REFRESHTOKEN.value)
        logger.info(f"{user_email} logged out successfully.")
        return ApplicationServices.application_response(
            HttpStatusCodeEnum.OK,
            ResponseMessageEnum.LoggedOut,
            True,
            {}
        )
