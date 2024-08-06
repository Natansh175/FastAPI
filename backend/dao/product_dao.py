from backend import sql_dynamic
from backend.db.db import SessionLocal

db = SessionLocal()


class ProductDAO:
    @staticmethod
    def create_product(product_data):
        sql_dynamic.insert_data('product_table', product_data)

    @staticmethod
    def read_products(skip, limit, sort_criteria, search_keyword):
        product_vo_list = sql_dynamic.view_data_all('product_table',
                                                    'product',
                                                    5, skip,
                                                    limit, sort_criteria,
                                                    search_keyword)
        return product_vo_list

    @staticmethod
    def read_product_by_id(view_id):
        product_vo_list = sql_dynamic.view_data_by_id('product_table',
                                                      view_id, column_name="product_id")
        return product_vo_list

    @staticmethod
    def update_product(product_vo_list):
        sql_dynamic.update_data('product_table', product_vo_list)
