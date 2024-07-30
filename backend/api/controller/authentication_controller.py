from fastapi import APIRouter, Request, Response, Form
import jwt

from backend.dto.register_dto import RegisterDTO
from backend.services.authentication_services import AuthenticationServices
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum

authentication = APIRouter(
    prefix="/authentication",
    tags=["authentication"],
)



@authentication.post("/register_user")
def register_user(response: Response, user_info: RegisterDTO):

    authentication_services = AuthenticationServices()

    try:
        if not user_info:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.BadRequest,
                False,
                {}
            )

        response_data = authentication_services.insert_user(user_info)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Register user exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


@authentication.post("/login")
async def user_login(request: Request, response: Response,
                     email: str = Form(...),
                     password: str = Form(...)):
    try:
        if not email or not password:
            response.status_code = HttpStatusCodeEnum.UNAUTHORIZED
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.BadRequest,
                False,
                {}
            )

        authentication_services = AuthenticationServices()
        response_data = authentication_services.app_login(email,
                                                          password,
                                                          response)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Login validate Controller exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


@authentication.post("/logout")
async def user_logout(request: Request, response: Response):
    try:
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
            print(data)
            user_email = data['public_id']

            authentication_services = AuthenticationServices()
            response_data = authentication_services.app_logout(
                user_email, response)

            response.status_code = response_data.get('status_code')
            return response_data.get('response_message')

    except Exception as exception:
        print(f"Logout Controller exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)
