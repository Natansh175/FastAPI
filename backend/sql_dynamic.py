from sqlalchemy import or_, inspect

from backend.db.db import Base, SessionLocal
from backend.services.app_services import ApplicationServices
from backend.enum.http_enum import ResponseMessageEnum

# Creating DataBase Session
db = SessionLocal()


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
        db.rollback()
        print(f"Insert Data exception in dynamic file : {exception}")
        return ApplicationServices.handle_exception(exception, True)


# To view all available data in specific table
def view_data_all(table_name: str, columns_start_from: str,
                  important_columns: int, skip, limit,
                  sort_criteria, search):
    try:
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            if sort_criteria is None:
                sorting_column = 'created_date'
            else:
                sorting_column = sort_criteria

            query = db.query(table).filter(table.c.is_deleted == 0)

            # Had to add slicing just because product table
            # Which had image name and path columns starting from 'product' also.
            if search is not None:
                search_conditions = [
                    table.c[column.name].like(f"%{search}%")
                    for column in inspect(table).c
                    if columns_start_from in column.name][:important_columns]

                if search_conditions:
                    query = query.filter(or_(*search_conditions)).order_by(sorting_column)
            query = query.order_by(sorting_column).offset(skip).limit(limit)
            return query.all()

        else:
            return ResponseMessageEnum.TableNotFound

    except Exception as exception:
        print(f"View Data exception in dynamic file : {exception}")
        return ApplicationServices.handle_exception(exception, True)


# To Retrieve single data from specific table by ID
def view_data_by_id(table_name: str, view_id: int, column_name: str):
    try:
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            data_column = getattr(table.c, column_name)
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
    update as well as partial delete functionalities.
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
