import os
import uuid
import logging
from datetime import datetime
from pathlib import Path

from backend.vo.product_vo import ProductVO
from backend.dao.category_dao import CategoryDAO
from backend.dao.subcategory_dao import SubCategoryDAO
from backend.dao.product_dao import ProductDAO
from backend.dto.product_dto import ProductDTO, UpdateProductDataDTO
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler
file_handler = logging.FileHandler('product_services.log')
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


IMAGE_PATH = "static/user_resources/images"


def fk_delete_check(category_id: int, subcategory_id: int):
    """
    Checks if the category and subcategory are not marked as deleted.

    Args:
        category_id (int): ID of the category to check.
        subcategory_id (int): ID of the subcategory to check.

    Returns:
        bool: True if both are not deleted, otherwise False.
    """
    category_dao = CategoryDAO()
    subcategory_dao = SubCategoryDAO()

    category_vo_list = category_dao.read_category_immutable(category_id)
    subcategory_vo_list = subcategory_dao.read_subcategory_immutable(subcategory_id)

    if category_vo_list is not None and subcategory_vo_list is not None:
        return True
    else:
        pass


class ProductServices:
    # Service class for managing products in the application.
    @staticmethod
    def admin_insert_product(category_id: int, subcategory_id: int,
                             image_filename: str, image_data: bytes, product: ProductDTO):
        """
        Inserts a new product into the database after validating its category and subcategory.

        Args:
            category_id (int): ID of the category the product belongs to.
            subcategory_id (int): ID of the subcategory the product belongs to.
            image_filename (str): Filename of the product image.
            image_data (bytes): Byte data of the product image.
            product (ProductDTO): Data transfer object for the product.

        Returns:
            dict: Response message and status.
        """
        logger.info("Inserting a new product in database")
        try:
            if fk_delete_check(category_id, subcategory_id) is None:
                logger.warning(f"No Category or SubCategory found with "
                               f"category ID: {category_id} and "
                               f"subcategory ID: {subcategory_id}")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.NoCategorySubCategoryFound, False, {})

            if product.product_quantity > 0 and product.product_price > 0:
                unique_id = uuid.uuid4()
                image_unique_filename = f"{unique_id}_{image_filename}"
                image_path = Path(IMAGE_PATH) / image_unique_filename

                # Save the image
                with open(image_path, "wb") as image_file:
                    image_file.write(image_data)

                product_vo = ProductVO()
                product_dao = ProductDAO()

                product_vo.product_name = product.product_name
                product_vo.product_description = product.product_description
                product_vo.product_price = product.product_price
                product_vo.product_quantity = product.product_quantity
                product_vo.product_image_name = image_unique_filename
                product_vo.product_image_path = f"/{IMAGE_PATH}/{image_unique_filename}"
                product_vo.is_deleted = False
                product_vo.created_date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
                product_vo.edited_date = ""
                product_vo.product_category_id = category_id
                product_vo.product_subcategory_id = subcategory_id

                product_dao.create_product(product_data=product_vo)

                logger.info(f"Product created: {product_vo.product_name}")

                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.CREATED,
                    ResponseMessageEnum.ProductCreated, True, {})

            else:
                logger.warning("Product insertion failed due to invalid input data")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.UNPROCESSABLE_ENTITY,
                    ResponseMessageEnum.ProductUnprocessableEntity, False, {})

        except Exception as exception:
            logger.error(f"Product Insert Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_read_products():
        """
        Reads all products from the database and filters out the ones that
        are marked as deleted.

        Returns:
           list of dict: Response message and product data.
        """
        logger.info("Reading all products from the database")
        try:
            product_dao = ProductDAO()

            product_data = product_dao.read_products()
            if product_data:
                data_to_show = [
                    {
                        "product_id": product.product_id,
                        "product_name": product.product_name,
                        "product_description": product.product_description,
                        "product_price": product.product_price,
                        "product_quantity": product.product_quantity
                    }
                    for product in product_data
                    if fk_delete_check(product.product_category_id,
                                       product.product_subcategory_id)
                ]

                if data_to_show:
                    logger.info("Products retrieved successfully")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK, ResponseMessageEnum.OK, True,
                        {"Detail": data_to_show})

                else:
                    logger.info("No Products found in database")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        ResponseMessageEnum.NoProductFound,
                        False, {"Detail": ResponseMessageEnum.NoProductFound})

            else:
                logger.info("No Products found in database or the "
                            "category/subcategory marked as deleted.")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.NoProductFound,
                    False, {"Detail": ResponseMessageEnum.NoProductFound})

        except Exception as exception:
            logger.error(f"Product Read Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_delete_product(product_id: int):
        """
        Marks a product as deleted.

        Args:
            product_id (int): ID of the product to mark as deleted.

        Returns:
            dict: Response message and status.
        """
        logger.info(f"Deleting product with ID: {product_id} from database")
        try:
            product_dao = ProductDAO()
            product_vo_list = product_dao.read_product_mutable(product_id)

            if product_vo_list is not None and product_vo_list.is_deleted == 0:

                delete_check = fk_delete_check(
                    product_vo_list.product_category_id, product_vo_list.product_subcategory_id)

                if delete_check is None:
                    logger.warning(f"No Category or SubCategory found with ID: {product_id}")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        ResponseMessageEnum.ProductNotFound, False, {})

                else:
                    product_vo_list.is_deleted = True
                    product_dao.update_product(product_vo_list)

                    logger.info(f"Product deleted with ID: {product_id}")

                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK, ResponseMessageEnum.ProductDeleted, True, {})

            elif product_vo_list is None or product_vo_list.is_deleted == 1:
                logger.warning("Product is already marked as deleted or product does not exist")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.ProductNotFound, False, {})

        except Exception as exception:
            logger.error(f"Product Delete Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_update_product_data(product_update_id: int, product_update_data: UpdateProductDataDTO):
        """
        Updates product data.

        Args:
            product_update_id (int): ID of the product to update.
            product_update_data (UpdateProductDataDTO): Data transfer object with updated product data.

        Returns:
            dict: Response message and status.
        """
        logger.info(f"Updating product Data of Product ID: {product_update_id}")
        try:
            product_dao = ProductDAO()
            product_vo_list = product_dao.read_product_mutable(product_update_id)

            if (product_update_data.product_name == "" or
                    product_update_data.product_description == "" or
                    product_update_data.product_price == 0 or
                    product_update_data.product_quantity == 0):
                logger.warning("Data updating failed due to invalid data")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.UNPROCESSABLE_ENTITY,
                    ResponseMessageEnum.ProductUnprocessableEntity, False, {})

            if product_vo_list is not None and product_vo_list.is_deleted == 0:
                delete_value = fk_delete_check(
                    product_vo_list.product_category_id, product_vo_list.product_subcategory_id)

                if delete_value is None:
                    logger.info(f"Product with "
                                f"category_id: {product_vo_list.product_category_id} and "
                                f"subcategory_id: {product_vo_list.product_subcategory_id} "
                                f"does not exist or marked as deleted.")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        ResponseMessageEnum.ProductNotFound, False, {})

                else:
                    # Updating just the fields that are changed by user
                    product_data = product_update_data.model_dump(exclude_unset=True)
                    for key, value in product_data.items():
                        setattr(product_vo_list, key, value)

                    for data in product_data.values():
                        if data == "" or 0:
                            logger.warning(
                                "Category update failed due to invalid input data")

                            return ApplicationServices.application_response(
                                HttpStatusCodeEnum.UNPROCESSABLE_ENTITY,
                                ResponseMessageEnum.CategoryUnprocessableEntity,
                                False,
                                {}
                            )
                    product_vo_list.edited_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')

                    product_dao.update_product(product_vo_list=product_vo_list)

                    logger.info(f"Product updated: {product_update_id}")

                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK,
                        ResponseMessageEnum.ProductUpdated, True, {})

            elif product_vo_list is None or product_vo_list.is_deleted == 1:
                logger.warning("Product is already marked as deleted or product does not exist")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.ProductNotFound, False, {})

        except Exception as exception:
            logger.error(f"Product Update_Data Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_update_product_image(update_image_id: int, update_image_name: str, product_image_data: bytes):
        """
        Updates the image for a given product ID.

        Args:
            update_image_id (int): ID of the product whose image needs to be updated.
            update_image_name (str): New image filename.
            product_image_data (bytes): Byte data of the new image.

        Returns:
            dict: Response message and status.
        """
        logger.info(f"Updating image of product_id: {update_image_id}")
        try:
            product_dao = ProductDAO()

            product_vo_list = product_dao.read_product_mutable(update_image_id)

            if product_vo_list is not None and product_vo_list.is_deleted == 0:

                delete_check = fk_delete_check(
                    product_vo_list.product_category_id, product_vo_list.product_subcategory_id)

                if delete_check is None:
                    logger.info(f"Product with "
                                f"category_id: {product_vo_list.product_category_id} and "
                                f"subcategory_id: {product_vo_list.product_subcategory_id} "
                                f"does not exist or marked as deleted.")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        ResponseMessageEnum.ProductNotFound, False, {})

                else:
                    previous_product_image = product_vo_list.product_image_name
                    os.remove(os.path.join(IMAGE_PATH, previous_product_image))

                    unique_id = uuid.uuid4()
                    image_unique_filename = f"{unique_id}_{update_image_name}"
                    image_path = Path(IMAGE_PATH) / image_unique_filename

                    # Save the new image
                    with open(image_path, "wb") as image_file:
                        image_file.write(product_image_data)

                    product_vo_list.product_image_name = image_unique_filename
                    product_vo_list.edited_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')
                    product_vo_list.product_image_path = f"/{IMAGE_PATH}/{image_unique_filename}"
                    product_dao.update_product(product_vo_list=product_vo_list)

                    logger.info(f"Product image updated: {update_image_id}")

                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK,
                        ResponseMessageEnum.ImageUpdated, True, {})

            elif product_vo_list is None or product_vo_list.is_deleted == 1:
                logger.warning("Product is already marked as deleted or product does not exist")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.ProductNotFound, False, {})

        except Exception as exception:
            logger.error(f"Product Update_Image Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)
