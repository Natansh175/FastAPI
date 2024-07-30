import logging
from datetime import datetime

from backend.dao.category_dao import CategoryDAO
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.services.app_services import ApplicationServices
from backend.vo.category_vo import CategoryVO

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler for all logs
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler for error logs
file_handler = logging.FileHandler('backend/logs/category_services.log')
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class CategoryServices:
    # Service class for managing categories in the application

    @staticmethod
    def admin_insert_category(category):
        """
        Insert a new category into the database.

        Args:
            category (CategoryDTO): The data transfer object containing category details.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info("Inserting a new category")
        try:
            category_vo = CategoryVO()
            category_dao = CategoryDAO()

            category_vo.category_name = category.category_name
            category_vo.category_description = category.category_description
            category_vo.category_count = category.category_count
            category_vo.is_deleted = False
            category_vo.created_date = datetime.strftime(datetime.now(),
                                                         '%Y-%m-%d %H:%M:%S')
            category_vo.edited_date = datetime.strftime(datetime.now(),
                                                        '%Y-%m-%d %H:%M:%S')

            category_dao.create_category(category_vo)
            logger.info(
                f"Category '{category.category_name}' inserted successfully")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.CREATED,
                ResponseMessageEnum.CategoryCreated,
                True,
                {}
            )

        except Exception as exception:
            logger.error(f"Category Insert Service Exception: {exception}",
                         exc_info=True)
            ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_read_categories():
        """
        Retrieve all categories from the database.

        Returns:
            list of dict: The response from the application services,
            including status and data.
        """
        logger.info("Reading all categories")
        try:
            category_dao = CategoryDAO()
            category_data = category_dao.read_categories()

            if category_data:
                data_to_show = [
                    {
                        "category_id": category.category_id,
                        "category_name": category.category_name,
                        "category_description": category.category_description,
                        "category_count": category.category_count
                    }
                    for category in category_data
                ]
                logger.info("Categories retrieved successfully")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.OK, ResponseMessageEnum.OK, True,
                    data=data_to_show
                )

            logger.info("No categories found")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.NoCategoryFound,
                False,
                data=ResponseMessageEnum.NoCategoryFound
            )
        except Exception as exception:
            logger.error(f"Category Read Service Exception: {exception}",
                         exc_info=True)
            ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_delete_category(category_id: int):
        """
        Delete a category by marking it as deleted.

        Args:
            category_id (int): The ID of the category to be deleted.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info(f"Deleting category with ID {category_id}")
        try:
            category_vo = CategoryVO()
            category_dao = CategoryDAO()

            category_vo.category_id = category_id
            category_vo.is_deleted = True
            category_dao.update_category(category_vo)

            logger.info(
                f"Category with ID {category_id} marked as deleted")

            return ApplicationServices.application_response(
                HttpStatusCodeEnum.OK, ResponseMessageEnum.CategoryDeleted,
                True, {}
            )

        except Exception as exception:
            logger.error(f"Category Delete Service Exception: {exception}",
                         exc_info=True)
            ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_update_category(category_update_dto):
        """
        Update the details of an existing category.

        Args:
            category_update_dto (CategoryUpdateDTO): The data transfer object containing updated category details.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info(f"Updating subcategory with ID {category_update_dto.subcategory_id}")
        try:
            category_vo = CategoryVO()
            category_dao = CategoryDAO()
            for key, value in category_update_dto.model_dump(
                    exclude_unset=True).items():
                setattr(category_vo, key, value)

            category_vo.edited_date = datetime.strftime(
                datetime.now(), '%Y-%m-%d %H:%M:%S')
            category_dao.update_category(category_vo)

            logger.info(
                f"Category with ID {category_update_dto.category_id} updated "
                f"successfully")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.OK,
                ResponseMessageEnum.CategoryUpdated, True, {}
            )

        except Exception as exception:
            logger.error(f"Category Update Service Exception: {exception}",
                         exc_info=True)
            ApplicationServices.handle_exception(exception, True)
