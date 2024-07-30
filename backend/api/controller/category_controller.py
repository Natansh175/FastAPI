from fastapi import APIRouter, Response, Request

from backend.dto.category_dto import CategoryDTO, CategoryUpdateDTO
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.enum.authentication_enum import AuthenticationEnum
from backend.services.app_services import ApplicationServices
from backend.services.authentication_services import login_required
from backend.services.category_services import CategoryServices

category = APIRouter(
    prefix="/category",
    tags=["category"],
)


@category.post("/insert_category/")
@login_required(role=AuthenticationEnum.ADMIN_ROLE)
async def create_category(category_insert: CategoryDTO, request: Request,
                          response: Response):
    try:
        category_services = CategoryServices()
        if not category_insert:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.BadRequest, False, data={})

        response_data = category_services.admin_insert_category(
            category_insert)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Category Insert Controller Exception: {exception}")
        ApplicationServices.handle_exception(exception, is_raise=True)


@category.get("/get_categories/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.USER_ROLE])
async def read_categories(request: Request, response: Response):
    try:
        category_services = CategoryServices()
        response_data = category_services.admin_read_categories()

        response.status_code = response_data.get('status_code')
        return response_data.get('data')

    except Exception as exception:
        print(f"Category Read Controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, is_raise=True)


@category.delete("/delete_category/")
@login_required(role=AuthenticationEnum.ADMIN_ROLE)
async def delete_category(category_id: int, request: Request,
                          response: Response):
    try:
        category_services = CategoryServices()
        if not category_id:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.CategoryNotFound, False, data={})

        response_data = category_services.admin_delete_category(category_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Category Delete Controller Exception: {exception}")
        ApplicationServices.handle_exception(exception, is_raise=True)


@category.put("/update_category/")
@login_required(role=AuthenticationEnum.ADMIN_ROLE)
async def update_category(category_update_dto: CategoryUpdateDTO,
                          request: Request, response: Response):
    try:
        category_services = CategoryServices()
        if not category_update_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.BadRequest, False, data={})

        response_data = category_services.admin_update_category(
            category_update_dto)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Category Update Controller Exception: {exception}")
        ApplicationServices.handle_exception(exception, is_raise=True)
