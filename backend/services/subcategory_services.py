from datetime import datetime

from fastapi import HTTPException

from backend.dao.category_dao import CategoryDAO
from backend.dao.subcategory_dao import SubCategoryDAO
from backend.vo.subcategory_vo import SubCategoryVO
from backend.dto.subcategory_dto import SubCategoryDTO, UpdateSubCategoryDTO


# A function to check whether the category is deleted or not Prior of performing any activity on subcategory table.
def category_delete_check(category_id: int):

    category_dao = CategoryDAO()
    category_vo_list = category_dao.read_category(category_id)
    if category_vo_list is not None:
        return True
    else:
        pass


def admin_insert_subcategory(subcategory: SubCategoryDTO, category_id: int):
    try:
        category_dao = CategoryDAO()
        subcategory_vo = SubCategoryVO()
        subcategory_dao = SubCategoryDAO()

        category_data = category_dao.read_category(category_id=category_id)

        if not category_data:
            raise HTTPException(status_code=500, detail="Cannot find category of this ID")

        subcategory_vo.subcategory_name = subcategory.subcategory_name
        subcategory_vo.subcategory_description = subcategory.subcategory_description
        subcategory_vo.subcategory_count = subcategory.subcategory_count
        subcategory_vo.is_active = False
        subcategory_vo.created_date = datetime.strftime(datetime.now(), '%d-%m-%Y' '%H:%M')
        subcategory_vo.edited_date = ""
        subcategory_vo.subcategory_category_id = category_id

        if category_data.is_deleted:
            raise HTTPException(status_code=500, detail="Cannot find category of this ID")
        else:
            subcategory_dao.create_subcategory(subcategory_vo)
            return subcategory_vo

    except HTTPException as ex:
        raise ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


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
                if category_dao.read_category(
                    subcategory.subcategory_category_id) is not None
            ]

            if data_to_show:
                return data_to_show
            else:
                raise HTTPException(detail="No Subcategories to show", status_code=404)
        else:
            raise HTTPException(detail="No subcategories to show", status_code=404)

    except HTTPException as ex:
        raise ex

    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=500)


def admin_delete_subcategory(subcategory_id: int):
    try:
        subcategory_dao = SubCategoryDAO()
        subcategory_vo_list = subcategory_dao.edit_subcategory(subcategory_id)

        if subcategory_vo_list is not None and subcategory_vo_list.is_deleted == 0:

            delete_value = category_delete_check(subcategory_vo_list.subcategory_category_id)

            if delete_value is None:
                raise HTTPException(status_code=404, detail="Cannot find subcategory with this ID")

            else:

                subcategory_vo_list.is_deleted = True
                subcategory_dao.update_subcategory(subcategory_vo_list)

                return {"Message": "SubCategory deleted successfully"}

        elif subcategory_vo_list is None or subcategory_vo_list.is_deleted == 1:
            return HTTPException(detail="Cannot find subcategory with this ID", status_code=500)

    except HTTPException as ex:
        raise ex

    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=500)


def admin_update_subcategory(update_subcategory_id: int, subcategory:
                             UpdateSubCategoryDTO):
    try:
        subcategory_dao = SubCategoryDAO()
        subcategory_vo_list = subcategory_dao.edit_subcategory(
            update_subcategory_id)

        if subcategory_vo_list is not None and subcategory_vo_list.is_deleted == 0:
            delete_value = category_delete_check(subcategory_vo_list.subcategory_category_id)

            if delete_value is None:
                raise HTTPException(status_code=500, detail="Cannot find subcategory with this ID")

            else:
                subcategory_data = subcategory.model_dump(exclude_unset=True)
                for key, value in subcategory_data.items():
                    setattr(subcategory_vo_list, key, value)

                subcategory_vo_list.edited_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')

                subcategory_dao.update_subcategory(
                    subcategory_vo_list=subcategory_vo_list)
                return subcategory_vo_list

        elif subcategory_vo_list is None or subcategory_vo_list.is_deleted == 1:
            raise HTTPException(status_code=404, detail="Cannot find subcategory with this ID")

    except HTTPException as ex:
        raise ex

    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=500)
