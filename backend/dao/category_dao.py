from backend import sql_dynamic
from opentelemetry import trace


class CategoryDAO:
    @staticmethod
    def create_category(category):
        sql_dynamic.insert_data('category_table', category)

    # To read one particular Category Data (Immutable)
    @staticmethod
    def read_category_by_id(view_id):
        category_vo_list = sql_dynamic.view_data_by_id('category_table',
                                                       view_id=view_id,
                                                       column_name="category_id")
        return category_vo_list

    # To show all inserted and not-deleted categories to user
    @staticmethod
    def read_categories(skip, limit, sort_criteria, search_keyword):
        with trace.get_tracer(__name__).start_as_current_span(
                "read_category_dao_span") as span:
            span.set_attribute("skip", skip)
            span.set_attribute("limit", limit)
            span.set_attribute("sort_criteria", sort_criteria)
            span.set_attribute("search_keyword", search_keyword)

            category_data = sql_dynamic.view_data_all('category_table',
                                                      'category',
                                                      4, skip,
                                                      limit, sort_criteria, search_keyword)
            return category_data

    @staticmethod
    def update_category(category_vo_list):
        sql_dynamic.update_data('category_table', category_vo_list)
