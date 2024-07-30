import logging

from datetime import datetime

from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.dao.category_dao import CategoryDAO
from backend.dao.subcategory_dao import SubCategoryDAO
from backend.vo.subcategory_vo import SubCategoryVO

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler for all logs
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler for error logs
file_handler = logging.FileHandler('backend/logs/subcategory_services.log')
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class SubCategoryServices:
    # Service class for managing subcategories in the application.
    @staticmethod
    def admin_insert_subcategory(subcategory):
        """
        Insert a new subcategory into the database.

        Args:
            subcategory (SubCategoryDTO): The data transfer object containing
            subcategory details and subcategory_category_id (int): The ID of
            the parent category.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info("Inserting a new subcategory")
        try:

            subcategory_vo = SubCategoryVO()
            subcategory_dao = SubCategoryDAO()

            subcategory_vo.subcategory_name = subcategory.subcategory_name
            subcategory_vo.subcategory_description = subcategory.subcategory_description
            subcategory_vo.subcategory_count = subcategory.subcategory_count
            subcategory_vo.created_date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            subcategory_vo.edited_date = ""
            subcategory_vo.subcategory_category_id = subcategory.subcategory_category_id

            subcategory_dao.create_subcategory(subcategory_vo)
            logger.info(f"Subcategory '"
                        f"{subcategory.subcategory_name}' inserted successfully")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.CREATED,
                ResponseMessageEnum.SubCategoryCreated, True, subcategory_vo)

        except Exception as exception:
            logger.error(f"SubCategory Insert Service Exception: {exception}", exc_info=True)
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_read_subcategories():
        """
        Retrieve all subcategories from the database.

        Returns:
            list of dict: The response from the application services,
            including status and data.
        """
        logger.info("Reading all subcategories")
        try:
            category_dao = CategoryDAO()
            subcategory_dao = SubCategoryDAO()
            subcategory_data = subcategory_dao.read_subcategories()

            if subcategory_data:
                data_to_show = [
                    {
                        "subcategory_id": subcategory.subcategory_id,
                        "subcategory_name": subcategory.subcategory_name,
                        "subcategory_description": subcategory.subcategory_description,
                        "subcategory_count": subcategory.subcategory_count
                    }
                    for subcategory in subcategory_data
                    if category_dao.read_category_by_id(
                        subcategory.subcategory_category_id) is not None
                ]

                if data_to_show:
                    logger.info("subcategories retrieved successfully")
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK, ResponseMessageEnum.OK, True,
                        data=data_to_show)

                logger.warning("No valid subcategories found")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND, ResponseMessageEnum.NoSubCategoryFound,
                    False,
                    data=ResponseMessageEnum.NoSubCategoryFound)

            logger.warning("No subcategories found")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.NoSubCategoryFound,
                False,
                data=ResponseMessageEnum.NoSubCategoryFound)

        except Exception as exception:
            logger.error(f"SubCategory Read Service Exception: {exception}", exc_info=True)
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_delete_subcategory(subcategory_id):
        """
        Mark a subcategory as deleted.

        Args:
            subcategory_id (int): The ID of the subcategory to be deleted.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info(f"Deleting subcategory with ID {subcategory_id}")
        try:
            subcategory_vo = SubCategoryVO()
            subcategory_dao = SubCategoryDAO()

            subcategory_vo.subcategory_id = subcategory_id
            subcategory_vo.is_deleted = True
            subcategory_dao.update_subcategory(subcategory_vo)

            logger.info(f"Subcategory with ID {subcategory_id} marked as deleted")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.OK, ResponseMessageEnum.SubCategoryDeleted, True, {})

        except Exception as exception:
            logger.error(f"SubCategory Delete Service Exception: {exception}", exc_info=True)
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_update_subcategory(subcategory_update_dto):
        """
        Update the details of an existing subcategory.

        Args:
            subcategory_update_dto (SubCategoryDTO): The data transfer object containing
            updated subcategory details.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info(f"Updating subcategory with ID {subcategory_update_dto.subcategory_id}")
        try:
            subcategory_vo = SubCategoryVO()
            subcategory_dao = SubCategoryDAO()

            for key, value in subcategory_update_dto.model_dump(
                    exclude_unset=True).items():
                setattr(subcategory_vo, key, value)

            subcategory_vo.edited_date = datetime.strftime(
                datetime.now(), '%Y-%m-%d %H:%M:%S')
            subcategory_dao.update_subcategory(subcategory_vo)

            logger.info(f"Subcategory with ID {subcategory_update_dto.subcategory_id} "
                        f"updated successfully")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.OK,
                ResponseMessageEnum.SubCategoryUpdated,
                True, {})

        except Exception as exception:
            logger.error(f"SubCategory Update Service Exception: {exception}", exc_info=True)
            ApplicationServices.handle_exception(exception, is_raise=True)
