from backend.vo.categoryVO import CategoryVO
from backend.dao.categoryDAO import CategoryDAO
from backend.dto.categoryDTO import UpdateCategoryDto, CategoryDto
from fastapi import HTTPException
from datetime import datetime
from backend.enum.http_enum import ErrorCode, ErrorDetail


class CategoryServices:
    def adminInsertCategory(self, category: CategoryDto):
        try:
            category_vo = CategoryVO()
            category_dao = CategoryDAO()

            category_vo.category_name = category.category_name
            category_vo.category_description = category.category_description
            category_vo.category_count = category.category_count
            category_vo.is_deleted = False
            category_vo.created_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')
            category_vo.edited_date = ""

            category_dao.createCategory(category_vo)
            return category

        except Exception as ex:
            raise HTTPException(detail=str(ex), status_code=500)


    def adminReadCategories(self):
        try:
            category_dao = CategoryDAO()
            category_data = category_dao.readCategories()

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
                return data_to_show

            else:
                raise HTTPException(detail="No categories to show", status_code=404)

        except HTTPException as ex:
            raise ex

        except Exception as ex:
            raise HTTPException(detail=str(ex), status_code=500)


    def adminDeleteCategory(self, category_id: int):
        try:
            category_dao = CategoryDAO()
            category_vo_list = category_dao.editCategory(category_id)

            if category_vo_list is not None:
                category_vo_list.is_deleted = True
                category_dao.updateCategory(category_vo_list)

                return {"Message": "Category Deleted Successfully"}

            elif category_vo_list is None:
                return HTTPException(detail="Cannot find category with this ID", status_code=500)

        except Exception as ex:
            raise HTTPException(detail=str(ex), status_code=500)


    def adminUpdateCategory(self, update_category_id: int, category: UpdateCategoryDto):
        try:
            category_dao = CategoryDAO()
            category_vo_list = category_dao.editCategory(update_category_id)
            if category_vo_list is not None and category_vo_list.is_deleted == 0:

                update_data = category.model_dump(exclude_unset=True)

                for key, value in update_data.items():
                    setattr(category_vo_list, key, value)

                category_vo_list.edited_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')
                category_dao.updateCategory(category_vo_list=category_vo_list)

                return category_vo_list

            else:
                raise HTTPException(status_code=404, detail="Cannot find category with this ID")

        except HTTPException as ex:
            raise ex

        except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))
