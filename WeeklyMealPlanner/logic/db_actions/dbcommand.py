from sqlite3.dbapi2 import Cursor, IntegrityError, OperationalError
from typing import Any, Dict, List, Tuple
from WeeklyMealPlanner.logic.db_actions.dbconnection import DBConnection


class DBCommand(DBConnection):
    '''
        General class that handles database functions.
    '''
    cmd: Cursor
    _table_name: str
    _headers: str
    _values: str


    def __init__(self) -> None:
        self._connect_db()

    def _execute(self, command: str) -> None:
        '''
        Pass in a command to be executed in the database.
        '''
        self._connect_db()
        self.cmd.execute(command)

    def create_table(self, table_name: str, headers: List[str]) -> str:
        ''''
        Create a new table for the month in the db.
        Pass in a name for the table.
        '''
        self._table_name = table_name
        self._headers = ", ".join(str(header) for header in headers)
        try:
            self._execute(
                f'''
                    CREATE TABLE IF NOT EXISTS {self._table_name} ({self._headers})
                '''
            )
            self._commit_disconnect_db()
            return f'Success! Table "{self._table_name}" has been created.'
        except OperationalError as e:
            return f'Error: "{e}". Unable to create table!'
        except IntegrityError as e:
            return f'Error: "{e}". Table already exists!'

    def drop_table(self, table_name: str) -> str:
        '''
        Delete a specified table from the db.
        Pass in name of the table to be deleted.
        '''
        self._table_name = table_name
        try:
            self._execute(
                f'''
                DROP TABLE {self._table_name}
                '''
            )
            self._commit_disconnect_db()
            return f'Success! Table "{self._table_name}" has been deleted.'
        except OperationalError as e:
            return f'Error: "{e}". Unable to perform delete operation!'

    def update_table(self, table_name: str, headers: List[str], values: List[str]) -> Any:
        '''
        Update the contents of a table. Pass in the command with headers and values.
        Format will be:
            INSERT INTO table_name (headers)
            VALUES (values)
        '''
        self._table_name = table_name
        self._headers = ", ".join(str(header) for header in headers)
        self._values = ", ".join(str(value) for value in values)

        try:
            self._execute(
                f'''
                INSERT INTO {self._table_name} ({self._headers})
                VALUES ({self._values})
                '''
            )
            self._commit_disconnect_db()
            return f'Successfully updated {self._table_name}'
        except OperationalError as e:
            return f'Error: {e}. Unable to update entry!'
        except IntegrityError as e:
            return f'Error: {e}. Meal already exists in db for the specified date.'

    def delete_entry(self, table_name: str, header: str, value: str) -> str:
        '''
        Deletes a specified entry from a specified table. Pass in the name of the table, column (header) to search in and record (value) to delete.
        '''
        self._table_name = table_name
        try:
            self._execute(
                f'''
                DELETE FROM {self._table_name}
                WHERE {header} = '{value}'
                '''
            )
            self._commit_disconnect_db()
            return f'Successfuly deleted {value}'
        except OperationalError as e:
            return f'Error {e}. Unable to delete entry!'

    def edit_entry(self, table_name: str, primary_key: str, primary_key_value: Any, **kwargs: Dict[str, str or float]) -> str:
        '''
        Edit entries within the database.
        '''
        self._table_name = table_name
        set_values: str = ''

        for k,v in kwargs.items():
            set_values = set_values + f"{k} = {v}, "
        set_values = set_values[:-2]

        try:
            self._execute(
                f'''
                UPDATE {self._table_name}
                SET {set_values}
                WHERE {primary_key} = {primary_key_value}
                '''
            )
            self._commit_disconnect_db()
            return f'Successfully updated {self._table_name}'
        except OperationalError as e:
            return f'Error: {e}. Update table {self._table_name} failed.'
    
    def filter_records(self, table_name: str, header: str, value: str) -> List[Tuple[Any]]:
        '''
        Filter specific records from specified table. Pass in table name, column name as 'header' and entry to filter by as 'value'.
        '''
        self._table_name = table_name
        self._execute(
            f'''
            SELECT *
            FROM {self._table_name}
            WHERE {header} = '{value}'
            '''
        )
        filtered_values: List[Tuple[Any]] = self.cmd.fetchall()
        self._commit_disconnect_db()
        return filtered_values

    def find_record(self, table_name: str, header: str, value: str) -> Tuple[str or float]:
        '''
        Filter specific records from specified table. Pass in table name, column name as 'header' and entry to filter by as 'value'.
        '''
        self._table_name = table_name
        self._execute(
            f'''
            SELECT *
            FROM {self._table_name}
            WHERE {header} = '{value}'
            '''
        )
        record: Tuple[Any] = self.cmd.fetchone()
        self._commit_disconnect_db()
        return record
