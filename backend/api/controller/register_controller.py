from fastapi import APIRouter, Request, Response

from backend.dto.register_dto import RegisterDTO
from backend.services.register_services import RegisterServices
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum

register = APIRouter(
    prefix="/register",
    tags=["register yourself!"],
)


@register.post("/register_user")
def register_user(response: Response, user_info: RegisterDTO):

    register_services = RegisterServices()

    try:
        if not user_info:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.BadRequest,
                False,
                {}
            )

        response_data = register_services.insert_user(user_info)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Register user exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)
