from fastapi import APIRouter, Response

from backend.dto.subcategory_dto import SubCategoryDTO, UpdateSubCategoryDTO
from backend.services.subcategory_services import SubCategoryServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.services.app_services import ApplicationServices

subCategory = APIRouter(
    prefix="/subcategory",
    tags=["subcategory"],
)


@subCategory.post("/insert_subcategory/")
async def create_subcategory(subcategory_insert: SubCategoryDTO,
                             category_id: int, response: Response):
    try:
        subcategory_services = SubCategoryServices()
        if not subcategory_insert:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(HttpStatusCodeEnum.BAD_REQUEST,
                                                            ResponseMessageEnum.BadRequest, False, data={})

        response_data = subcategory_services.admin_insert_subcategory(subcategory_insert, category_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"SubCategory Insert controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


@subCategory.get("/get_subcategories/")
async def read_subcategories(response: Response):
    try:
        subcategory_services = SubCategoryServices()
        response_data = subcategory_services.admin_read_subcategories()

        response.status_code = response_data.get('status_code')
        return response_data['data']['Detail']

    except Exception as exception:
        print(f"SubCategory Read controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


@subCategory.delete("/delete_subcategory/")
async def delete_subcategory(subcategory_id: int, response: Response):
    try:
        subcategory_services = SubCategoryServices()
        if not subcategory_id:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.SubCategoryNotFound, False, data={})

        response_data = subcategory_services.admin_delete_subcategory(subcategory_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"SubCategory Delete controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


@subCategory.put("/update_subcategory/")
async def update_subcategory(update_subcategory_id: int, subcategory_update:
                             UpdateSubCategoryDTO, response: Response):
    try:
        subcategory_services = SubCategoryServices()
        if not subcategory_update:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST, ResponseMessageEnum.BadRequest, False, data={})

        response_data = subcategory_services.admin_update_subcategory(update_subcategory_id, subcategory_update)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"SubCategory Update controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)
