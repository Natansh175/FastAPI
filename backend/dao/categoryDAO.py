from backend.vo.categoryVO import CategoryVO
from backend import sql_dynamic
from backend.db.db import SessionLocal

db = SessionLocal()


class CategoryDAO:
    def createCategory(self, category):
        sql_dynamic.insert_data('category_table', category)

    # To read one particular Category Data
    def readCategory(self, category_id: int):
        category_vo_list = sql_dynamic.view_data_by_id('category_table', view_id=category_id)
        return category_vo_list

    # To show all inserted and not-deleted categories to user
    def readCategories(self):
        category_data = sql_dynamic.view_data_all('category_table')
        return category_data

    def editCategory(self, update_category_id: int):
        category_vo_list = db.get(CategoryVO, update_category_id)
        return category_vo_list

    def updateCategory(self, category_vo_list):
        sql_dynamic.update_data('category_table', category_vo_list)
