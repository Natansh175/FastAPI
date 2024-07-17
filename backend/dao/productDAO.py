from backend import sql_dynamic
from backend.vo.productVO import ProductVO
from backend.db.db import SessionLocal

db = SessionLocal()


class ProductDAO:
    def createProduct(self, product_data):
        sql_dynamic.insert_data('product_table', product_data)

    def readProducts(self):
        product_vo_list = sql_dynamic.view_data_all('product_table')
        return product_vo_list

    def editProduct(self, update_product_id: int):
        product_vo_list = db.get(ProductVO, update_product_id)
        return product_vo_list

    def updateProduct(self, product_vo_list):
        sql_dynamic.update_data('product_table', product_vo_list)
