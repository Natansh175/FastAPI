import logging
from fastapi import APIRouter, Response, Request, Query
from typing import Optional, Any

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

# Initialize logger
logger = logging.getLogger(__name__)

# File_handler for error logs
file_handler = logging.FileHandler('backend/logs/category/category_controller.log')
logger.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


@category.post("/insert_category/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def create_category(category_insert: CategoryDTO, request: Request,
                          response: Response):
    try:
        category_services = CategoryServices()
        if not category_insert:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.BadRequest, False, data={})

        user_id = request.state.user.get('username')

        response_data = category_services.admin_insert_category(
            category_insert, user_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        logger.error(f"Category Insert Controller Exception: {exception}",
                     exc_info=True)
        ApplicationServices.handle_exception(exception, is_raise=True)


@category.get("/get_categories/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE,
                      AuthenticationEnum.USER_ROLE,
                      AuthenticationEnum.SELLER_ROLE])
async def read_categories(request: Request, response: Response,
                          limit: Optional[int] =
                          Query(default=10, description="Items per page"),
                          page: int = Query(default=1,
                                            description="Page number",
                                            ge=1),
                          sort_by: Optional[str] = Query(None,
                                                         description="Sort by field"),
                          search_keyword: Optional[Any] =
                          Query(None, description="Search for specific keyword")
                          ):
    try:
        category_services = CategoryServices()

        user_id = request.state.user.get('username')

        response_data = category_services.admin_read_categories(user_id,
                                                                limit, page,
                                                                sort_by,
                                                                search_keyword)

        response.status_code = response_data.get('status_code')
        return response_data.get('data')

    except Exception as exception:
        logger.error(f"Category Read Controller Exception: {exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, is_raise=True)


@category.delete("/delete_category/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def delete_category(category_id: int, request: Request,
                          response: Response):
    try:
        category_services = CategoryServices()
        if not category_id:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.CategoryNotFound, False, data={})

        user_id = request.state.user.get('username')

        response_data = category_services.admin_delete_category(category_id,
                                                                user_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        logger.error(f"Category Delete Controller Exception: {exception}",
                     exc_info=True)
        ApplicationServices.handle_exception(exception, is_raise=True)


@category.put("/update_category/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def update_category(category_update_dto: CategoryUpdateDTO,
                          request: Request, response: Response):
    try:
        category_services = CategoryServices()
        if not category_update_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.BadRequest, False, data={})

        user_id = request.state.user.get('username')

        response_data = category_services.admin_update_category(
            category_update_dto, user_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        logger.error(f"Category Update Controller Exception: {exception}", exc_info=True)
        ApplicationServices.handle_exception(exception, is_raise=True)
