from backend.db.db import Base, SessionLocal
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum

# Creating DataBase Session
db = SessionLocal()


# To get the 'id column name' according to table
def get_table_id(table_name: str):
    which_table = table_name.split("_")
    table_id = which_table[0] + "_" + "id"

    return table_id


# To insert new row in specific table
def insert_data(table_name: str, data: dict):
    try:
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            db.add(data)
            db.commit()
        else:
            return ResponseMessageEnum.TableNotFound

    except Exception as exception:
        print(f"Insert Data exception in dynamic file : {exception}")
        return ApplicationServices.handle_exception(exception, True)


# To view all available data in specific table
def view_data_all(table_name: str):
    try:
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            view_stmt = db.query(table).filter(table.c.is_deleted == 0).all()
            return view_stmt
        else:
            return ResponseMessageEnum.TableNotFound

    except Exception as exception:
        print(f"View Data exception in dynamic file : {exception}")
        return ApplicationServices.handle_exception(exception, True)


# To Retrieve single data from specific table by ID
def view_data_by_id(table_name: str, view_id: int):
    try:
        table = Base.metadata.tables.get(table_name)
        if table is not None:

            table_id = get_table_id(table_name)
            data_column = getattr(table.c, table_id)
            view_stmt = db.query(table).filter(data_column == view_id).first()
            if view_stmt is None:
                pass
            elif view_stmt is not None:
                if view_stmt.is_deleted:
                    pass
                else:
                    return view_stmt
        else:
            return ResponseMessageEnum.TableNotFound

    except Exception as exception:
        print(f"View Data by ID exception in dynamic file : {exception}")
        return ApplicationServices.handle_exception(exception, True)


# To Retrieve single data from specific table by username
def view_data_by_email(table_name: str, email: str):
    try:
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            view_stmt = db.query(table).filter(table.c.login_username == email).first()

            if view_stmt is None:
                pass
            else:
                return view_stmt
        else:
            return ResponseMessageEnum.TableNotFound

    except Exception as exception:
        print(f"View Data by Email exception in dynamic file : {exception}")
        return ApplicationServices.handle_exception(exception, True)


def update_data(table_name: str, data: dict):
    """
    To update specific data in specific table This function is being used for
    update as well as partial delete functionalities
    """
    try:
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            db.merge(data)
            db.commit()
        else:
            return ResponseMessageEnum.TableNotFound

    except Exception as exception:
        print(f"Update Data exception in dynamic file : {exception}")
        return ApplicationServices.handle_exception(exception, True)
