from backend import sql_dynamic


class SubCategoryDAO:
    @staticmethod
    def create_subcategory(subcategory_data):
        sql_dynamic.insert_data('subcategory_table', subcategory_data)

    # to read one particular Subcategory Data
    @staticmethod
    def read_subcategory_by_id(subcategory_id):
        subcategory_vo_list = sql_dynamic.view_data_by_id('subcategory_table', subcategory_id)
        return subcategory_vo_list

    # to read all subcategories
    @staticmethod
    def read_subcategories():
        subcategory_data = sql_dynamic.view_data_all('subcategory_table')
        return subcategory_data

    @staticmethod
    def update_subcategory(subcategory_vo_list):
        sql_dynamic.update_data('subcategory_table', subcategory_vo_list)
