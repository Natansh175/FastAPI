import logging
from fastapi import APIRouter, Request, Response, Form

from backend.dto.register_dto import RegisterDTO
from backend.services.authentication_services import AuthenticationServices
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum

authentication = APIRouter(
    prefix="/authentication",
    tags=["authentication"],
)

# Initialize logger
logger = logging.getLogger(__name__)

# File_handler for error logs
file_handler = logging.FileHandler('backend/logs/authentication/authentication_controller.log')
logger.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


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
        logger.error(f"Register user exception: {exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)


@authentication.post("/login")
async def user_login(response: Response,
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
        logger.error(f"Login validate Controller exception: {exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)


@authentication.post("/logout")
async def user_logout(request: Request, response: Response):
    try:
        user_email = request.state.user.get('username')

        authentication_services = AuthenticationServices()
        response_data = authentication_services.app_logout(
            user_email, response)

        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        logger.error(f"Logout Controller exception: {exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)
