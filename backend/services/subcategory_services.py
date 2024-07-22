from datetime import datetime

from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from backend.dao.category_dao import CategoryDAO
from backend.dao.subcategory_dao import SubCategoryDAO
from backend.vo.subcategory_vo import SubCategoryVO
from backend.dto.subcategory_dto import SubCategoryDTO, UpdateSubCategoryDTO


# A function to check whether the category is deleted or not Prior of
# performing any activity on subcategory table.
def category_delete_check(category_id: int):
    category_dao = CategoryDAO()
    category_vo_list = category_dao.read_category_immutable(category_id)

    if category_vo_list is not None:
        return True
    else:
        pass


class SubCategoryServices:
    @staticmethod
    def admin_insert_subcategory(subcategory: SubCategoryDTO, category_id: int):
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
            subcategory_vo.created_date = datetime.strftime(datetime.now(), '%d-%m-%Y' '%H:%M')
            subcategory_vo.edited_date = ""
            subcategory_vo.subcategory_category_id = category_id

            if (subcategory.subcategory_count == 0 or
                    subcategory.subcategory_name == "" or
                    subcategory.subcategory_description == ""):

                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.UNPROCESSABLE_ENTITY,
                    ResponseMessageEnum.SubCategoryUnprocessableEntity,
                    False, {})

            else:
                subcategory_dao.create_subcategory(subcategory_vo)
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.CREATED,
                    ResponseMessageEnum.SubCategoryCreated, True, subcategory_vo)

        except Exception as exception:
            print(f"SubCategory Insert Service Exception: {exception}")
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_read_subcategories():
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
                    if category_dao.read_category_immutable(subcategory.subcategory_category_id) is not None
                ]

                if data_to_show:
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK, ResponseMessageEnum.OK, True,
                        {"Detail": data_to_show})

                else:
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND, ResponseMessageEnum.NoSubCategoryFound,
                        False, {"Detail": ResponseMessageEnum.NoSubCategoryFound})
            else:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.NoSubCategoryFound,
                    False, {"Detail": ResponseMessageEnum.NoSubCategoryFound})

        except Exception as exception:
            print(f"SubCategory Read Service Exception: {exception}")
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_delete_subcategory(subcategory_id: int):
        try:
            subcategory_dao = SubCategoryDAO()
            subcategory_vo_list = subcategory_dao.read_subcategory_mutable(subcategory_id)

            if subcategory_vo_list is not None and subcategory_vo_list.is_deleted == 0:

                delete_value = category_delete_check(subcategory_vo_list.subcategory_category_id)

                if delete_value is None:

                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        ResponseMessageEnum.SubCategoryNotFound,
                        False,
                        {})

                else:

                    subcategory_vo_list.is_deleted = True
                    subcategory_dao.update_subcategory(subcategory_vo_list)

                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK, ResponseMessageEnum.SubCategoryDeleted, True, {})

            elif subcategory_vo_list is None or subcategory_vo_list.is_deleted == 1:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.SubCategoryNotFound,
                    False,
                    {})

        except Exception as exception:
            print(f"SubCategory Delete Service Exception: {exception}")
            ApplicationServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def admin_update_subcategory(update_subcategory_id: int, subcategory:
                                 UpdateSubCategoryDTO):
        try:
            subcategory_dao = SubCategoryDAO()
            subcategory_vo_list = subcategory_dao.read_subcategory_mutable(
                update_subcategory_id)

            if subcategory.subcategory_name == "" or subcategory.subcategory_description == "" or subcategory.subcategory_count == 0:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.UNPROCESSABLE_ENTITY,
                    ResponseMessageEnum.SubCategoryUnprocessableEntity,
                    False, {})

            if subcategory_vo_list is not None and subcategory_vo_list.is_deleted == 0:
                delete_value = category_delete_check(subcategory_vo_list.subcategory_category_id)

                if delete_value is None:
                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        ResponseMessageEnum.SubCategoryNotFound,
                        False,
                        {})

                else:
                    subcategory_data = subcategory.model_dump(exclude_unset=True)
                    for key, value in subcategory_data.items():
                        setattr(subcategory_vo_list, key, value)

                    subcategory_vo_list.edited_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')

                    subcategory_dao.update_subcategory(subcategory_vo_list)

                    return ApplicationServices.application_response(
                        HttpStatusCodeEnum.OK,
                        ResponseMessageEnum.SubCategoryUpdated,
                        True,
                        subcategory_vo_list)

            elif subcategory_vo_list is None or subcategory_vo_list.is_deleted == 1:
                return ApplicationServices.application_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.SubCategoryNotFound,
                    False,
                    {})

        except Exception as exception:
            print(f"SubCategory Update Service Exception: {exception}")
            ApplicationServices.handle_exception(exception, is_raise=True)
