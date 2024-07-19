from backend import sql_dynamic
from backend.vo.product_vo import ProductVO
from backend.db.db import SessionLocal

db = SessionLocal()


class ProductDAO:
    @staticmethod
    def create_product(product_data):
        sql_dynamic.insert_data('product_table', product_data)

    @staticmethod
    def read_products():
        product_vo_list = sql_dynamic.view_data_all('product_table')
        return product_vo_list

    @staticmethod
    def edit_product(update_product_id: int):
        product_vo_list = db.get(ProductVO, update_product_id)
        return product_vo_list

    @staticmethod
    def update_product(product_vo_list):
        sql_dynamic.update_data('product_table', product_vo_list)
