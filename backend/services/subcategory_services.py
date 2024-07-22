from datetime import datetime
import logging

from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.dao.category_dao import CategoryDAO
from backend.dao.subcategory_dao import SubCategoryDAO
from backend.vo.subcategory_vo import SubCategoryVO
from backend.dto.subcategory_dto import SubCategoryDTO, UpdateSubCategoryDTO

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler for all logs
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler for error logs
file_handler = logging.FileHandler('subcategory_services.log')
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def category_delete_check(category_id: int) -> bool:
    """
    Check whether the specified category is deleted or not.

    Args:
        category_id (int): The ID of the category to check.

    Returns:
        bool: True if the category is not deleted, otherwise False.
    """
    category_dao = CategoryDAO()
    category_vo_list = category_dao.read_category_immutable(category_id)

    return category_vo_list is not None


class SubCategoryServices:
    """Service class for managing subcategories in the application."""

    @staticmethod
    def admin_insert_subcategory(subcategory: SubCategoryDTO, category_id: int) -> dict:
        """
        Insert a new subcategory into the database.

        Args:
            subcategory (SubCategoryDTO): The data transfer object containing subcategory details.
            category_id (int): The ID of the parent category.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info("Inserting a new subcategory")
        try:
            category_dao = CategoryDAO()
            subcategory_vo = SubCategoryVO()
            subcategory_dao = SubCategoryDAO()

            category_data = category_dao.read_category_immutable(category_id=category_id)

            if category_data is None or category_data.is_deleted:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.CategoryNotFound, False, {})

            subcategory_vo.subcategory_name = subcategory.subcategory_name
            subcategory_vo.subcategory_description = subcategory.subcategory_description
            subcategory_vo.subcategory_count = subcategory.subcategory_count
            subcategory_vo.is_active = False
            subcategory_vo.created_date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            subcategory_vo.edited_date = ""
            subcategory_vo.subcategory_category_id = category_id

            if (subcategory.subcategory_count == 0 or
                    subcategory.subcategory_name == "" or
                    subcategory.subcategory_description == ""):
                logger.warning("Subcategory insertion failed due to invalid input data")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.UNPROCESSABLE_ENTITY,
                    ResponseMessageEnum.SubCategoryUnprocessableEntity,
                    False, {})

            subcategory_dao.create_subcategory(subcategory_vo)
            logger.info(f"Subcategory '{subcategory_vo.subcategory_name}' inserted successfully")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.CREATED,
                ResponseMessageEnum.SubCategoryCreated, True, subcategory_vo)

        except Exception as exception:
            logger.error(f"SubCategory Insert Service Exception: {exception}", exc_info=True)
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_read_subcategories() -> dict:
        """
        Retrieve all subcategories from the database.

        Returns:
            list of dict: The response from the application services,
            including status and data.
        """
        logger.info("Reading all subcategories")
        try:
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
                    if category_delete_check(subcategory.subcategory_category_id)
                ]

                if data_to_show:
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK, ResponseMessageEnum.OK, True,
                        {"Detail": data_to_show})

                logger.warning("No valid subcategories found")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND, ResponseMessageEnum.NoSubCategoryFound,
                    False, {"Detail": ResponseMessageEnum.NoSubCategoryFound})

            logger.warning("No subcategories found")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.NoSubCategoryFound,
                False, {"Detail": ResponseMessageEnum.NoSubCategoryFound})

        except Exception as exception:
            logger.error(f"SubCategory Read Service Exception: {exception}", exc_info=True)
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_delete_subcategory(subcategory_id: int) -> dict:
        """
        Mark a subcategory as deleted.

        Args:
            subcategory_id (int): The ID of the subcategory to be deleted.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info(f"Deleting subcategory with ID {subcategory_id}")
        try:
            subcategory_dao = SubCategoryDAO()
            subcategory_vo_list = subcategory_dao.read_subcategory_mutable(subcategory_id)

            if subcategory_vo_list is not None and not subcategory_vo_list.is_deleted:
                if not category_delete_check(subcategory_vo_list.subcategory_category_id):
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        ResponseMessageEnum.SubCategoryNotFound,
                        False,
                        {})

                subcategory_vo_list.is_deleted = True
                subcategory_dao.update_subcategory(subcategory_vo_list)
                logger.info(f"Subcategory with ID {subcategory_id} marked as deleted")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.OK, ResponseMessageEnum.SubCategoryDeleted, True, {})

            logger.warning(f"Subcategory with ID {subcategory_id} not found or already deleted")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.SubCategoryNotFound,
                False,
                {})

        except Exception as exception:
            logger.error(f"SubCategory Delete Service Exception: {exception}", exc_info=True)
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_update_subcategory(update_subcategory_id: int, subcategory: UpdateSubCategoryDTO) -> dict:
        """
        Update the details of an existing subcategory.

        Args:
            update_subcategory_id (int): The ID of the subcategory to be updated.
            subcategory (UpdateSubCategoryDTO): The data transfer object containing updated subcategory details.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info(f"Updating subcategory with ID {update_subcategory_id}")
        try:
            subcategory_dao = SubCategoryDAO()
            subcategory_vo_list = subcategory_dao.read_subcategory_mutable(update_subcategory_id)

            if (subcategory.subcategory_name == "" or
                    subcategory.subcategory_description == "" or
                    subcategory.subcategory_count == 0):
                logger.warning("Subcategory update failed due to invalid input data")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.UNPROCESSABLE_ENTITY,
                    ResponseMessageEnum.SubCategoryUnprocessableEntity,
                    False, {})

            if subcategory_vo_list is not None and not subcategory_vo_list.is_deleted:
                if not category_delete_check(subcategory_vo_list.subcategory_category_id):
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        ResponseMessageEnum.SubCategoryNotFound,
                        False,
                        {})

                subcategory_data = subcategory.model_dump(exclude_unset=True)
                for key, value in subcategory_data.items():
                    setattr(subcategory_vo_list, key, value)

                subcategory_vo_list.edited_date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
                subcategory_dao.update_subcategory(subcategory_vo_list)

                logger.info(f"Subcategory with ID {update_subcategory_id} updated successfully")
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.OK,
                    ResponseMessageEnum.SubCategoryUpdated,
                    True,
                    {})

            logger.warning(f"Subcategory with ID {update_subcategory_id} not found or already deleted")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.SubCategoryNotFound,
                False,
                {})

        except Exception as exception:
            logger.error(f"SubCategory Update Service Exception: {exception}", exc_info=True)
            ApplicationServices.handle_exception(exception, is_raise=True)
