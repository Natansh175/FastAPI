from fastapi import APIRouter, UploadFile, File, Form, Response

from backend.dto.product_dto import ProductDTO, UpdateProductDataDTO
from backend.services.product_services import ProductServices
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum


product = APIRouter(
    prefix="/product",
    tags=["product"],
)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
IMAGE_PATH = "static/user_resources/images"


@product.post("/insert_product/")
async def create_product(category_id: int,
                         subcategory_id: int,
                         response: Response,
                         product_name: str = Form(...),
                         product_description: str = Form(...),
                         product_price: int = Form(...),
                         product_quantity: int = Form(...),
                         product_image: UploadFile = File(...)
                         ):
    try:
        product_services = ProductServices()
        # To check if uploaded file type is allowed
        if product_image.content_type not in ALLOWED_IMAGE_TYPES:
            response.status_code = HttpStatusCodeEnum.UNSUPPORTED_MEDIA_TYPE
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.UNSUPPORTED_MEDIA_TYPE,
                ResponseMessageEnum.InvalidImageType, False, {})

        # Read image data
        product_image_data = await product_image.read()

        product_data = ProductDTO(
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            product_quantity=product_quantity,
        )

        response_data = product_services.admin_insert_product(
            category_id,
            subcategory_id,
            product_image.filename,
            product_image_data,
            product_data
        )
        response.status_code = response_data.get('status_code')
        return response_data.get('response_message')

    except Exception as exception:
        print(f"Product Insert Controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


@product.get("/get_products/")
async def read_products(response: Response):
    try:
        product_services = ProductServices()
        response_data = product_services.admin_read_products()

        response.status_code = response_data.get('status_code')
        return response_data['data']['Detail']

    except Exception as exception:
        print(f"Product Read Controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)



@product.delete("/delete_product/")
async def delete_product(product_id: int, response: Response):
    try:
        product_services = ProductServices()
        if not product_id:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.ProductNotFound, False, data={})

        response_data = product_services.admin_delete_product(product_id)
        response.status_code = response_data.get('status_code')
        return response_data['response_message']

    except Exception as exception:
        print(f"Product Delete Controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


@product.put("/update_product_data/")
async def update_product(product_update_id: int, product_update_data:
                         UpdateProductDataDTO, response: Response):
    try:
        product_services = ProductServices()
        if not product_update_data:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.BAD_REQUEST, ResponseMessageEnum.BadRequest,
                False, data={})

        response_data = product_services.admin_update_product_data(
            product_update_id, product_update_data)
        response.status_code = response_data.get('status_code')
        return response_data['response_message']

    except Exception as exception:
        print(f"Product Update_Data Controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)


@product.put("/update_product_image/")
async def update_product_image(product_id: int, response: Response,
                               product_image: UploadFile = File(...)):
    try:
        product_services = ProductServices()
        # To check if uploaded file type is allowed
        if product_image.content_type not in ALLOWED_IMAGE_TYPES:
            response.status_code = HttpStatusCodeEnum.UNSUPPORTED_MEDIA_TYPE
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.UNSUPPORTED_MEDIA_TYPE,
                ResponseMessageEnum.InvalidImageType, False, {})

        # To read image data
        product_image_data = await product_image.read()

        response_data = product_services.admin_update_product_image(product_id,
                                                                    product_image.filename,
                                                                    product_image_data)
        response.status_code = response_data.get('status_code')
        return response_data['response_message']

    except Exception as exception:
        print(f"Product Update_Image Controller Exception: {exception}")
        return ApplicationServices.handle_exception(exception, True)
