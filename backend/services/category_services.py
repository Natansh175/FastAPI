from datetime import datetime

from backend.vo.category_vo import CategoryVO
from backend.dao.category_dao import CategoryDAO
from backend.dto.category_dto import UpdateCategoryDTO, CategoryDTO
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.services.app_services import ApplicationServices


class CategoryServices:
    @staticmethod
    def admin_insert_category(category: CategoryDTO):
        try:
            category_vo = CategoryVO()
            category_dao = CategoryDAO()

            category_vo.category_name = category.category_name
            category_vo.category_description = category.category_description
            category_vo.category_count = category.category_count
            category_vo.is_deleted = False
            category_vo.created_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')
            category_vo.edited_date = ""

            if category_vo.category_count > 0 and category_vo.category_name != "" and category_vo.category_description != "":
                category_dao.create_category(category_vo)

                return ApplicationServices.application_response(
                    status_code=HttpStatusCodeEnum.CREATED.value,
                    response_message=ResponseMessageEnum.CategoryCreated.value,
                    success=True,
                    data=category.model_dump())

            else:
                return ApplicationServices.application_response(
                    status_code=HttpStatusCodeEnum.UNPROCESSABLE_ENTITY.value,
                    response_message=ResponseMessageEnum.CategoryUnprocessableEntity.value,
                    success=False,
                    data={})

        except Exception as exception:
            print(f"Category Insert Service Exception: {exception}")
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_read_categories():
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

                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.OK, ResponseMessageEnum.OK, success=True,
                    data=data_to_show)

            else:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND, ResponseMessageEnum.CategoryNotFound,
                    success=False,
                    data={"Detail": ResponseMessageEnum.NoCategoryFound})


        except Exception as exception:
            print(f"Category Read Service Exception: {exception}")
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_delete_category(category_id: int):
        try:
            category_dao = CategoryDAO()
            category_vo_list = category_dao.read_category_mutable(category_id)

            if category_vo_list is not None and not category_vo_list.is_deleted:
                category_vo_list.is_deleted = True
                category_dao.update_category(category_vo_list)

                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.OK, ResponseMessageEnum.CategoryDeleted, True, data={})

            elif category_vo_list is None or category_vo_list.is_deleted:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND, ResponseMessageEnum.CategoryNotFound, False,
                    data={})

        except Exception as exception:
            print(f"Category Delete Service Exception: {exception}")
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_update_category(update_category_id: int, category:
                              UpdateCategoryDTO):
        try:
            category_dao = CategoryDAO()
            category_vo_list = category_dao.read_category_mutable(update_category_id)
            if category_vo_list is not None and category_vo_list.is_deleted == 0:

                update_data = category.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(category_vo_list, key, value)

                category_vo_list.edited_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')

                if category.category_count == 0 or category.category_name == "" or category.category_description == "":

                    return ApplicationServices.application_response(
                        status_code=HttpStatusCodeEnum.UNPROCESSABLE_ENTITY.value,
                        response_message=ResponseMessageEnum.CategoryUnprocessableEntity.value,
                        success=False,
                        data={})

                else:
                    category_dao.update_category(category_vo_list)

                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK,
                        ResponseMessageEnum.CategoryUpdated, True, data=category_vo_list)

            else:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.CategoryNotFound, False, {})

        except Exception as exception:
            print(f"Category Update Service Exception: {exception}")
            ApplicationServices.handle_exception(exception, is_raise=True)
