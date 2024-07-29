from backend.vo.subcategory_vo import SubCategoryVO
from backend import sql_dynamic
from backend.db.db import SessionLocal

db = SessionLocal()


class SubCategoryDAO:
    @staticmethod
    def create_subcategory(subcategory_data):
        sql_dynamic.insert_data('subcategory_table', subcategory_data)

    # to read one particular Subcategory Data
    @staticmethod
    def read_subcategory_immutable(subcategory_id):
        subcategory_vo_list = sql_dynamic.view_data_by_id('subcategory_table', subcategory_id)
        return subcategory_vo_list

    # to read all subcategories
    @staticmethod
    def read_subcategories():
        subcategory_data = sql_dynamic.view_data_all('subcategory_table')
        return subcategory_data

    # To read one particular Category Data (Mutable)
    # Problem here!!
    # Not getting updated with db without reloading API.
    # @staticmethod
    # def read_subcategory_mutable(update_subcategory_id: int):
    #     subcategory_vo_list = db.get(SubCategoryVO, update_subcategory_id)
    #     return subcategory_vo_list

    @staticmethod
    def read_subcategory_mutable(update_subcategory_id: int):
        subcategory_vo_list = sql_dynamic.view_data_mutable(
            'subcategory_table', update_subcategory_id)
        return subcategory_vo_list

    @staticmethod
    def update_subcategory(subcategory_vo_list):
        sql_dynamic.update_data('subcategory_table', subcategory_vo_list)
