import logging
from fastapi import APIRouter, Response, Request, Query, BackgroundTasks
from typing import Optional, Any

from backend.dto.subcategory_dto import SubCategoryDTO, SubCategoryUpdateDTO
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.enum.authentication_enum import AuthenticationEnum
from backend.services.subcategory_services import SubCategoryServices
from backend.services.app_services import ApplicationServices
from backend.services.authentication_services import login_required


subCategory = APIRouter(
    prefix="/subcategory",
    tags=["subcategory"],
)

# Initialize logger
logger = logging.getLogger(__name__)

# File_handler for error logs
file_handler = logging.FileHandler('backend/logs/subcategory/subcategory_controller.log')
logger.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


@subCategory.post("/insert_subcategory/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def create_subcategory(subcategory_insert: SubCategoryDTO,
                             request: Request,
                             response: Response):
    try:
        subcategory_services = SubCategoryServices()
        if not subcategory_insert:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(HttpStatusCodeEnum.BAD_REQUEST,
                                                            ResponseMessageEnum.BadRequest,
                                                            False, data={})

        user_id = request.state.user.get('username')

        response_data = subcategory_services.admin_insert_subcategory(
            subcategory_insert, user_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        logger.error(f"SubCategory Insert controller Exception: "
                     f"{exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)


@subCategory.get("/get_subcategories/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE,
                      AuthenticationEnum.USER_ROLE,
                      AuthenticationEnum.SELLER_ROLE])
async def read_subcategories(request: Request, response: Response,
                             background_tasks: BackgroundTasks,
                             limit: Optional[int] =
                             Query(default=10, description="Items per page"),
                             page: int = Query(default=1,
                                               description="Page number",
                                               ge=1),
                             sort_by: Optional[str] = Query(None,
                                                            description="Sort by field"),
                             search_keyword: Optional[Any] =
                             Query(None, description="Search for specific "
                                                     "keyword")):
    try:
        subcategory_services = SubCategoryServices()

        user_id = request.state.user.get('username')

        response_data = subcategory_services.admin_read_subcategories(
            user_id, limit, page, sort_by, search_keyword, background_tasks)

        response.status_code = response_data.get('status_code')
        return response_data.get('data')

    except Exception as exception:
        logger.error(f"SubCategory Read controller Exception: {exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)


@subCategory.delete("/delete_subcategory/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def delete_subcategory(subcategory_id: int, request: Request,
                             response: Response):
    try:
        subcategory_services = SubCategoryServices()
        if not subcategory_id:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.SubCategoryNotFound, False, data={})

        user_id = request.state.user.get('username')

        response_data = subcategory_services.admin_delete_subcategory(
            subcategory_id, user_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        logger.error(f"SubCategory Delete controller Exception: "
                     f"{exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)


@subCategory.put("/update_subcategory/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def update_subcategory(subcategory_update_dto: SubCategoryUpdateDTO,
                             request: Request,
                             response: Response):
    try:
        subcategory_services = SubCategoryServices()
        if not subcategory_update_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST, ResponseMessageEnum.BadRequest, False, data={})

        user_id = request.state.user.get('username')

        response_data = subcategory_services.admin_update_subcategory(
            subcategory_update_dto, user_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        logger.error(f"SubCategory Update controller Exception: "
                     f"{exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)
