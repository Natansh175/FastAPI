from backend import sql_dynamic


class AuthenticationDAO:

    @staticmethod
    def insert_user(user_vo):
        sql_dynamic.insert_data('user_table', user_vo)

    @staticmethod
    def insert_login(login_vo):
        sql_dynamic.insert_data('login_table', login_vo)

    @staticmethod
    def read_user_by_email(email):
        login_vo_list = sql_dynamic.view_data_by_email('login_table',
                                                       email)
        return login_vo_list
