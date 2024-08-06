import logging
from fastapi import APIRouter, UploadFile, File, Form, Response, Request, Query
from typing import Any, Optional

from backend.dto.product_dto import ProductDTO, ProductDataUpdateDTO
from backend.services.product_services import ProductServices
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.enum.authentication_enum import AuthenticationEnum
from backend.services.authentication_services import login_required


product = APIRouter(
    prefix="/product",
    tags=["product"],
)

# Initialize logger
logger = logging.getLogger(__name__)

# File_handler for error logs
file_handler = logging.FileHandler('backend/logs/product/product_controller.log')
logger.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
IMAGE_PATH = "static/user_resources/images"


@product.post("/insert_product/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def create_product(category_id: int,
                         subcategory_id: int,
                         request: Request,
                         response: Response,
                         product_name: str = Form(...),
                         product_description: str = Form(...),
                         product_price: int = Form(...),
                         product_quantity: int = Form(...),
                         product_image: UploadFile = File(...)
                         ):
    try:
        product_services = ProductServices()

        user_id = request.state.user.get('username')

        # To check if uploaded file type is allowed
        if product_image.content_type not in ALLOWED_IMAGE_TYPES:
            logger.warning(f"{product_image.content_type} is not allowed by "
                           f"{user_id}.")
            response.status_code = HttpStatusCodeEnum.UNSUPPORTED_MEDIA_TYPE
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.UNSUPPORTED_MEDIA_TYPE,
                ResponseMessageEnum.InvalidImageType, False, {})

        # Read image data
        product_image_data = await product_image.read()

        product_data = ProductDTO(
            product_category_id=category_id,
            product_subcategory_id=subcategory_id,
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            product_quantity=product_quantity,
        )

        response_data = product_services.admin_insert_product(
            product_image.filename,
            product_image_data,
            product_data,
            user_id
        )
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        logger.error(f"Product Insert Controller Exception: {exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)


@product.get("/get_products/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE,
                      AuthenticationEnum.USER_ROLE,
                      AuthenticationEnum.SELLER_ROLE])
async def read_products(request: Request, response: Response,
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
        product_services = ProductServices()

        user_id = request.state.user.get('username')

        response_data = product_services.admin_read_products(user_id, limit,
                                                             page, sort_by,
                                                             search_keyword)

        response.status_code = response_data.get('status_code')
        return response_data.get('data')

    except Exception as exception:
        logger.error(f"Product Read Controller Exception: {exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)



@product.delete("/delete_product/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def delete_product(product_id: int, request: Request,
                         response: Response):
    try:
        product_services = ProductServices()
        if not product_id:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.ProductNotFound, False, data={})

        user_id = request.state.user.get('username')

        response_data = product_services.admin_delete_product(product_id, user_id)
        response.status_code = response_data.get('status_code')
        return response_data['response_message']

    except Exception as exception:
        logger.error(f"Product Delete Controller Exception: {exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)


@product.put("/update_product_data/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def update_product(product_update_data: ProductDataUpdateDTO, request: Request,
                         response: Response):
    try:
        product_services = ProductServices()
        if not product_update_data:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST, ResponseMessageEnum.BadRequest,
                False, data={})

        user_id = request.state.user.get('username')

        response_data = product_services.admin_update_product_data(
            product_update_data, user_id)
        response.status_code = response_data.get('status_code')
        return response_data['response_message']

    except Exception as exception:
        logger.error(f"Product Update_Data Controller Exception: "
                     f"{exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)


@product.put("/update_product_image/")
@login_required(role=[AuthenticationEnum.ADMIN_ROLE, AuthenticationEnum.SELLER_ROLE])
async def update_product_image(product_id: int, request: Request,
                               response: Response,
                               product_image: UploadFile = File(...)):
    try:
        product_services = ProductServices()

        user_id = request.state.user.get('username')

        # To check if uploaded file type is allowed
        if product_image.content_type not in ALLOWED_IMAGE_TYPES:
            logger.warning(f"{product_image.content_type} is not allowed by "
                           f"{user_id}.")
            response.status_code = HttpStatusCodeEnum.UNSUPPORTED_MEDIA_TYPE
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.UNSUPPORTED_MEDIA_TYPE,
                ResponseMessageEnum.InvalidImageType, False, {})

        # To read image data
        product_image_data = await product_image.read()

        response_data = product_services.admin_update_product_image(product_id,
                                                                    product_image.filename,
                                                                    product_image_data,
                                                                    user_id)

        response.status_code = response_data.get('status_code')
        return response_data['response_message']

    except Exception as exception:
        logger.error(f"Product Update_Image Controller Exception: "
                     f"{exception}", exc_info=True)
        return ApplicationServices.handle_exception(exception, True)
