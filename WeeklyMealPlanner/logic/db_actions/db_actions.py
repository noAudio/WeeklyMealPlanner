from sqlite3 import connect
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor

class DbAccess:
    connection: Connection
    cmd: Cursor
    table_name: str

    def __init__(self) -> None:
        ''' Access the db to read, add, update, delete and/or remove tables and table entries '''
        self.connection: Connection = connect('foods.db')
        self.cmd: Cursor = self.connection.cursor()

    def create_table(self, month: str, year: int) -> str:
        '''
        Create a new table in the db.
        Parameters are Month and Year which are concatenated to make a table name.
        '''
        self.table_name = f'{month}_{year}'
        try:
            self.cmd.execute(
            f'''
            CREATE TABLE {self.table_name} (
                date INTEGER PRIMARY KEY,
                day VARCHAR,
                breakfast_primary VARCHAR,
                breakfast_secondary VARCHAR,
                breakfast_price FLOAT,
                supper_primary VARCHAR,
                supper_secondary VARCHAR,
                supper_price FLOAT,
                day_price FLOAT
            )
            '''
            )
            return f'Success! Table "{self.table_name}" has been created.'
        except sqlite3.OperationalError as e:
            error: str = f'Error: "{e}". Unable to create table!'
            # print(error)
            return error
    
    def delete_table(self, month: str, year: int) -> str:
        '''
        Delete a specified table from the db.
        Parameters are Month and Year which are concatenated to make the table name.
        '''
        self.table_name = f'{month}_{year}'
        try:
            self.cmd.execute(
                f'''
                DROP TABLE {self.table_name}
                '''
            )
            return f'Success! Table "{self.table_name}" has been deleted.'
        except sqlite3.OperationalError as e:
            error: str = f'Error: "{e}". Unable to perform delete operation!'
            print(error)
            return error
        

db_access: DbAccess = DbAccess()

# print(db_access.create_table(month='January', year=2020))
# db_access.delete_table(month='January', year=2020)