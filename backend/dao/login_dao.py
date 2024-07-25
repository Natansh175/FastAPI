from backend import sql_dynamic


class LoginDAO:

    @staticmethod
    def insert_login(login_vo):
        sql_dynamic.insert_data('login_table', login_vo)

    @staticmethod
    def read_data_by_mail(username):
        login_vo_list = sql_dynamic.view_data_by_username('login_table',
                                                          username)
        return login_vo_list
