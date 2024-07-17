from backend.vo.subCategoryVO import SubCategoryVO
from backend import sql_dynamic
from backend.db.db import SessionLocal

# noinspection PyMethodParameters
db = SessionLocal()


class SubCategoryDAO:
    def createSubCategory(self, subcategory_data):
        sql_dynamic.insert_data('subcategory_table', subcategory_data)

    # to read one particular Subcategory Data
    def readSubCategory(self, subcategory_id):
        subcategory_vo_list = sql_dynamic.view_data_by_id('subcategory_table', view_id=subcategory_id)
        return subcategory_vo_list

    # to read all subcategories
    def readSubCategories(self):
        subcategory_data = sql_dynamic.view_data_all('subcategory_table')
        return subcategory_data

    def editSubCategory(self, update_subcategory_id: int):
        subcategory_vo_list = db.get(SubCategoryVO, update_subcategory_id)
        return subcategory_vo_list

    def updateSubCategory(self, subcategory_vo_list):
        sql_dynamic.update_data('subcategory_table', subcategory_vo_list)
