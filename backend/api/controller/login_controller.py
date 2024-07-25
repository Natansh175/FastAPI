from fastapi import APIRouter, Request, Response, Form

from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.services.login_services import LoginServices

login = APIRouter(
    prefix="/login",
    tags=["login"],
)


@login.post("/login")
async def user_login(request: Request, response: Response,
                     username: str = Form(...),
                     password: str = Form(...)):
    try:
        if not username or not password:
            response.status_code = HttpStatusCodeEnum.UNAUTHORIZED
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.BadRequest,
                False,
                {}
            )

        login_services = LoginServices()
        response_data = login_services.validate_user(username, password)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Login validate Controller exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)
