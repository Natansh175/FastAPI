from backend import sql_dynamic


class RegisterDAO:

    @staticmethod
    def insert_user(user_vo):
        sql_dynamic.insert_data('user_table', user_vo)
