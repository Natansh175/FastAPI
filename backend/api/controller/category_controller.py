from fastapi import APIRouter, Response

from backend.dto.category_dto import CategoryDTO, UpdateCategoryDTO
from backend.services.category_services import CategoryServices
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum


category = APIRouter(
    prefix="/category",
    tags=["category"],
)


@category.post("/insert_category/")
async def create_category(category_insert: CategoryDTO, response: Response):
    try:
        category_services = CategoryServices()
        if not category_insert:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST.value
            return ApplicationServices.application_response(HttpStatusCodeEnum.BAD_REQUEST,
                                                            ResponseMessageEnum.BadRequest, False, data={})

        response_data = category_services.admin_insert_category(category_insert)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Category Insert Controller Exception: {exception}")
        ApplicationServices.handle_exception(exception, is_raise=True)


@category.get("/get_categories/")
async def read_categories(response: Response):
    category_services = CategoryServices()
    try:
        response_data = category_services.admin_read_categories()

        response.status_code = response_data.get('status_code')
        return response_data.get('data')

    except Exception as exception:
        print(f"Category Read Controller Exception: {exception}")
        ApplicationServices.handle_exception(exception, is_raise=True)


@category.delete("/delete_category/")
async def delete_category(category_id: int, response: Response):
    category_services = CategoryServices()
    try:
        if not category_id:
            ApplicationServices.application_response(HttpStatusCodeEnum.NOT_FOUND,
                                                     ResponseMessageEnum.CategoryNotFound, False, data={})

        response_data = category_services.admin_delete_category(category_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Category Read Controller Exception: {exception}")
        ApplicationServices.handle_exception(exception, is_raise=True)


@category.put("/update_category/", response_model=UpdateCategoryDTO)
async def update_category(update_category_id: int, category_update:
                          UpdateCategoryDTO):
    category_services = CategoryServices()
    return category_services.admin_update_category(update_category_id=update_category_id, category=category_update)
