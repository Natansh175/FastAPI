from backend.db.db import Base, SessionLocal

# Creating DataBase Session
db = SessionLocal()


# To get the 'id column name' according to table
def get_table_id(table_name: str):
    which_table = table_name.split("_")
    table_id = which_table[0] + "_" + "id"

    return table_id


# To insert new row in specific table
def insert_data(table_name: str, data: dict):
    table = Base.metadata.tables.get(table_name)
    if table is None:
        raise ValueError(f"Table {table_name} does not exist")

    db.add(data)
    db.commit()


# To view all available data in specific table
def view_data_all(table_name: str):
    table = Base.metadata.tables.get(table_name)
    if table is None:
        raise ValueError(f"Table {table_name} does not exist")

    view_stmt = db.query(table).filter(table.c.is_deleted == 0).all()
    return view_stmt


# To Retrieve single data from specific table by ID
def view_data_by_id(table_name: str, view_id: int):
    table = Base.metadata.tables.get(table_name)
    if table is None:
        raise ValueError(f"Table {table_name} does not exist")

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


# To update specific data in specific table
# This function is being used for update
# as well as partial delete functionalities
def update_data(table_name: str, data: dict):
    table = Base.metadata.tables.get(table_name)
    if table is None:
        raise ValueError(f"Table {table_name} does not exist")

    db.merge(data)
    db.flush()
    db.commit()
