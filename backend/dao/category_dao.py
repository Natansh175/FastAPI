from backend.vo.category_vo import CategoryVO
from backend import sql_dynamic
from backend.db.db import SessionLocal

db = SessionLocal()


class CategoryDAO:
    @staticmethod
    def create_category(category):
        sql_dynamic.insert_data('category_table', category)

    # To read one particular Category Data (Immutable)
    @staticmethod
    def read_category_immutable(category_id: int):
        category_vo_list = sql_dynamic.view_data_by_id('category_table', view_id=category_id)
        return category_vo_list

    # To show all inserted and not-deleted categories to user
    @staticmethod
    def read_categories():
        category_data = sql_dynamic.view_data_all('category_table')
        return category_data

    # To read one particular Category Data (Mutable)
    # Problem here!!
    # Not getting updated with db without reloading API.
    # @staticmethod
    # def read_category_mutable(update_category_id: int):
    #     category_vo_list = db.query(CategoryVO).filter(
    #         CategoryVO.category_id == update_category_id).first()
    #     return category_vo_list

    @staticmethod
    def read_category_mutable(update_category_id: int):
        category_vo_list = sql_dynamic.view_data_mutable('category_table',
                                                         update_category_id)
        return category_vo_list

    @staticmethod
    def update_category(category_vo_list):
        sql_dynamic.update_data('category_table', category_vo_list)
