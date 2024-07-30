import os
import uuid
import logging
from datetime import datetime
from pathlib import Path

from backend.vo.product_vo import ProductVO
from backend.dao.category_dao import CategoryDAO
from backend.dao.subcategory_dao import SubCategoryDAO
from backend.dao.product_dao import ProductDAO
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
file_handler = logging.FileHandler('backend/logs/product_services.log')
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


IMAGE_PATH = "static/user_resources/images"


class ProductServices:
    # Service class for managing products in the application.
    @staticmethod
    def admin_insert_product(image_filename, image_data: bytes, product):
        """
        Inserts a new product into the database after validating its category and subcategory.

        Args:
            image_filename (str): Filename of the product image.
            image_data (bytes): Byte data of the product image.
            product (ProductDTO): Data transfer object for the product.
            which contains the category ID and subcategory ID to which
            the product belongs to.

        Returns:
            dict: Response message and status.
        """
        logger.info("Inserting a new product in database")
        try:

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
            product_vo.product_category_id = product.product_category_id
            product_vo.product_subcategory_id = product.product_subcategory_id

            product_dao.create_product(product_vo)

            logger.info(f"Product created: {product.product_name}")

            return ApplicationServices.application_response(
                HttpStatusCodeEnum.CREATED,
                ResponseMessageEnum.ProductCreated, True, {})

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
            category_dao = CategoryDAO()
            subcategory_dao = SubCategoryDAO()
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
                    if category_dao.read_category_by_id(
                        product.product_category_id) is not None
                    and subcategory_dao.read_subcategory_by_id(
                            product.product_subcategory_id) is not None
                ]

                if data_to_show:
                    logger.info("Products retrieved successfully")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK, ResponseMessageEnum.OK, True,
                        data=data_to_show)

                else:
                    logger.info("No Products found in database or the "
                                "category/subcategory marked as deleted.")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        ResponseMessageEnum.NoProductFound,
                        False, data=ResponseMessageEnum.NoProductFound)

            else:
                logger.info("No Products found in database")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.NoProductFound,
                    False, data=ResponseMessageEnum.NoProductFound)

        except Exception as exception:
            logger.error(f"Product Read Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_delete_product(product_id):
        """
        Marks a product as deleted.

        Args:
            product_id (int): ID of the product to mark as deleted.

        Returns:
            dict: Response message and status.
        """
        logger.info(f"Deleting product with ID: {product_id} from database")
        try:
            product_vo = ProductVO()
            product_dao = ProductDAO()

            product_vo.product_id = product_id
            product_vo.is_deleted = True
            product_dao.update_product(product_vo)

            logger.info(f"Product deleted with ID: {product_id}")

            return ApplicationServices.application_response(
                HttpStatusCodeEnum.OK, ResponseMessageEnum.ProductDeleted, True, {})

        except Exception as exception:
            logger.error(f"Product Delete Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_update_product_data(product_update_data):
        """
        Updates product data.

        Args:
            product_update_data (ProductDataUpdateDTO): Data transfer object
            with updated product data.
            This comes with ID of the product to update.

        Returns:
            dict: Response message and status.
        """
        logger.info(f"Updating product Data of Product ID: "
                    f"{product_update_data.product_id}")
        try:
            product_vo = ProductVO()
            product_dao = ProductDAO()
            # Updating just the fields that are changed by user
            for key, value in product_update_data.model_dump(exclude_unset=True).items():
                setattr(product_vo, key, value)

            product_vo.edited_date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

            product_dao.update_product(product_vo)

            logger.info(f"Product updated: {product_update_data.product_id}")

            return ApplicationServices.application_response(
                HttpStatusCodeEnum.OK,
                ResponseMessageEnum.ProductUpdated, True, {})

        except Exception as exception:
            logger.error(f"Product Update_Data Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_update_product_image(update_image_id, update_image_name: str,
                                   product_image_data: bytes):
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
            product_vo = ProductVO()
            product_dao = ProductDAO()

            product_vo_list = product_dao.read_product_by_id(update_image_id)
            previous_product_image = product_vo_list.product_image_name
            os.remove(os.path.join(IMAGE_PATH, previous_product_image))

            unique_id = uuid.uuid4()
            image_unique_filename = f"{unique_id}_{update_image_name}"
            image_path = Path(IMAGE_PATH) / image_unique_filename

            # Save the new image
            with open(image_path, "wb") as image_file:
                image_file.write(product_image_data)

            product_vo.product_id = update_image_id
            product_vo.product_image_name = image_unique_filename
            product_vo.edited_date = datetime.strftime(datetime.now(),
                                                       '%Y-%m-%d %H:%M:%S')
            product_vo.product_image_path = f"/{IMAGE_PATH}/{image_unique_filename}"
            product_dao.update_product(product_vo)

            logger.info(f"Product image updated: {update_image_id}")

            return ApplicationServices.application_response(
                HttpStatusCodeEnum.OK,
                ResponseMessageEnum.ImageUpdated, True, {})

        except Exception as exception:
            logger.error(f"Product Update_Image Services Exception: {exception}")
            return ApplicationServices.handle_exception(exception, True)
