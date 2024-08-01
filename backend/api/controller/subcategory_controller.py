from fastapi import APIRouter, Response, Request
import jwt

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

        accesstoken = request.cookies.get(AuthenticationEnum.ACCESSTOKEN.value)
        data = jwt.decode(accesstoken,
                          algorithms=[AuthenticationEnum.HASH_ALGORITHM],
                          options={"verify_signature": False})
        user_id = data.get('public_id')

        response_data = subcategory_services.admin_insert_subcategory(
            subcategory_insert, user_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"SubCategory Insert controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


@subCategory.get("/get_subcategories/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE,
                      AuthenticationEnum.USER_ROLE,
                      AuthenticationEnum.SELLER_ROLE])
async def read_subcategories(request: Request, response: Response):
    try:
        subcategory_services = SubCategoryServices()

        accesstoken = request.cookies.get(AuthenticationEnum.ACCESSTOKEN.value)
        data = jwt.decode(accesstoken,
                          algorithms=[AuthenticationEnum.HASH_ALGORITHM],
                          options={"verify_signature": False})
        user_id = data.get('public_id')

        response_data = subcategory_services.admin_read_subcategories(user_id)

        response.status_code = response_data.get('status_code')
        return response_data.get('data')

    except Exception as exception:
        print(f"SubCategory Read controller Exception: {exception}")
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

        accesstoken = request.cookies.get(AuthenticationEnum.ACCESSTOKEN.value)
        data = jwt.decode(accesstoken,
                          algorithms=[AuthenticationEnum.HASH_ALGORITHM],
                          options={"verify_signature": False})
        user_id = data.get('public_id')

        response_data = subcategory_services.admin_delete_subcategory(
            subcategory_id, user_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"SubCategory Delete controller Exception: {exception}")
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

        accesstoken = request.cookies.get(AuthenticationEnum.ACCESSTOKEN.value)
        data = jwt.decode(accesstoken,
                          algorithms=[AuthenticationEnum.HASH_ALGORITHM],
                          options={"verify_signature": False})
        user_id = data.get('public_id')

        response_data = subcategory_services.admin_update_subcategory(
            subcategory_update_dto, user_id)
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"SubCategory Update controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)
