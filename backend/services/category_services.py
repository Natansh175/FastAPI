import logging
from datetime import datetime
from math import ceil

from backend.dao.category_dao import CategoryDAO
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.services.app_services import ApplicationServices
from backend.vo.category_vo import CategoryVO
from backend.excel_of_data import InsertDataIntoExcel

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
file_handler = logging.FileHandler('backend/logs/category/category_services.log')
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class CategoryServices:
    # Service class for managing categories in the application

    @staticmethod
    def admin_insert_category(category, user_id):
        """
        Insert a new category into the database.

        Args:
            category (CategoryDTO): The data transfer object containing category details.
            user_id (str): Name of the user accessing this endpoint.
        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info(f"{user_id} is inserting a new category.")
        try:
            category_vo = CategoryVO()
            category_dao = CategoryDAO()

            category_vo.category_name = category.category_name
            category_vo.category_description = category.category_description
            category_vo.category_count = category.category_count
            category_vo.is_deleted = False
            category_vo.created_date = datetime.strftime(datetime.now(),
                                                         '%d-%m-%Y %H:%M:%S')
            category_vo.edited_date = ""
            category_vo.created_by = user_id
            category_vo.edited_by = ""

            category_dao.create_category(category_vo)
            logger.info(
                f"Category '{category.category_name}' inserted successfully "
                f"by {user_id}.")
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
    def admin_read_categories(user_id, limit, page, sort_by, search_keyword,
                              background_tasks):
        """
        Retrieve all categories from the database.

        Args:
            user_id (str): Name of the user accessing this endpoint.
            limit (int): Maximum number of categories to return.
            page (int): Page number of the categories to return.
            sort_by (str): Sorting criteria.
            search_keyword (any): Search criteria.
            background_tasks (BackgroundTasks): Background tasks object.

        Returns:
            list of dict: The response from the application services,
            including status and data.
        """
        logger.info(f"{user_id} is reading all categories.")
        try:
            skip = (page - 1) * limit

            category_dao = CategoryDAO()
            insert_data_to_excel = InsertDataIntoExcel()

            category_data = category_dao.read_categories(skip, limit,
                                                         sort_by, search_keyword)

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
                total_count = len(data_to_show)
                total_pages = ceil(total_count / limit)

                max_pages_to_display = 5
                start_page = max(1, page - max_pages_to_display // 2)
                end_page = min(total_pages,
                               start_page + max_pages_to_display - 1)

                pagination_range = range(start_page, end_page + 1)

                background_tasks.add_task(insert_data_to_excel.admin_insert_data_excel,
                                          data_to_show, user_id,
                                          type_of_data="category_data")

                logger.info(f"Categories retrieved successfully by {user_id}.")
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
    def admin_delete_category(category_id, user_id):
        """
        Delete a category by marking it as deleted.

        Args:
            category_id (int): The ID of the category to be deleted.
            user_id (str): Name of the user accessing this endpoint.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info(f"{user_id} is deleting category with ID {category_id}.")
        try:
            category_vo = CategoryVO()
            category_dao = CategoryDAO()

            category_vo.category_id = category_id
            category_vo.is_deleted = True
            category_dao.update_category(category_vo)

            logger.info(
                f"{user_id} marked category_id:{category_id} as deleted.")

            return ApplicationServices.application_response(
                HttpStatusCodeEnum.OK, ResponseMessageEnum.CategoryDeleted,
                True, {}
            )

        except Exception as exception:
            logger.error(f"Category Delete Service Exception: {exception}",
                         exc_info=True)
            ApplicationServices.handle_exception(exception, True)

    @staticmethod
    def admin_update_category(category_update_dto, user_id):
        """
        Update the details of an existing category.

        Args:
            category_update_dto (CategoryUpdateDTO): The data transfer object containing updated category details.
            user_id (str): Name of the user accessing this endpoint.

        Returns:
            dict: The response from the application services, including status and message.
        """
        logger.info(f"{user_id} is updating category with ID"
                    f" {category_update_dto.category_id}.")
        try:
            category_vo = CategoryVO()
            category_dao = CategoryDAO()
            for key, value in category_update_dto.model_dump(
                    exclude_unset=True).items():
                setattr(category_vo, key, value)

            category_vo.edited_date = datetime.strftime(
                datetime.now(), '%d-%m-%Y %H:%M:%S')
            category_vo.edited_by = user_id
            category_dao.update_category(category_vo)

            logger.info(
                f"Category with ID {category_update_dto.category_id} updated "
                f"successfully by {user_id}.")
            return ApplicationServices.application_response(
                HttpStatusCodeEnum.OK,
                ResponseMessageEnum.CategoryUpdated, True, {}
            )

        except Exception as exception:
            logger.error(f"Category Update Service Exception: {exception}",
                         exc_info=True)
            ApplicationServices.handle_exception(exception, True)
