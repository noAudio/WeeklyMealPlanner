# from WeeklyMealPlanner.logic.data.foods import FoodClass, FoodType
from sqlite3 import connect
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from typing import Any, Dict, List, Tuple

class DbAccess:
    connection: Connection
    cmd: Cursor
    table_name: str

    def __init__(self) -> None:
        '''
        Access the db to read, add, update, delete and/or remove tables and table entries
        '''
        self.__connect_to_db__()
    
    def __connect_to_db__(self) -> None:
        self.connection: Connection = connect('foods.db')
        self.cmd: Cursor = self.connection.cursor()

    def create_month(self, month: str, year: int) -> str:
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
            self.connection.commit()
            self.connection.close()
            return f'Success! Table "{self.table_name}" has been created.'
        except sqlite3.OperationalError as e:
            error: str = f'Error: "{e}". Unable to create table!'
            # print(error)
            return error
    
    def delete_month(self, month: str, year: int) -> str:
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
            self.connection.commit()
            self.connection.close()
            return f'Success! Table "{self.table_name}" has been deleted.'
        except sqlite3.OperationalError as e:
            error: str = f'Error: "{e}". Unable to perform delete operation!'
            print(error)
            return error
        
    def add_food(self, food: Dict[str, Any]) -> str:
        '''
        Add a food to the db.
        Accepts a dictionary with food properties which are then added as an entry.
        '''
        self.table_name = f'Foods'
        try:
            self.cmd.execute(
                f'''
                INSERT INTO Foods (id, name, food_type, food_class, price)
                VALUES ('{food["id"]}', '{food["name"]}', '{food["food_type"]}', '{food["food_class"]}', {food["price"]})
                '''
            )
            self.connection.commit()
            self.connection.close()
            return f'Success! Added food item "{food["name"]}".'
        except sqlite3.OperationalError as e:
            return f'Error "{e}". Unable to update entry!'
        
    def delete_food(self, id: str, name: str) -> str:
        '''
        Delete a food from the db.
        Accepts the name and id of the food to be deleted.
        '''
        self.cmd.execute(
            f'''
            DELETE FROM Foods
            WHERE id = '{id}'
            '''
        )
        self.connection.commit()
        self.connection.close()
        return f'Succesfully deleted {name}.'
    
    def edit_food(self, id: str, food: Any) -> str:
        '''
        Edit a food in the db.
        Accepts the id of the food to be deleted and a dictionary of the new food values.
        '''
        self.cmd.execute(
            f'''
            UPDATE Foods
            SET name = '{food["name"]}', food_type = '{food["food_type"]}', food_class = '{food["food_class"]}', price = '{food["price"]}'
            WHERE id = '{id}'
            '''
        )
        self.connection.commit()
        self.connection.close()
        return f'Succesfully edited food.'
    
    def foods_by_foodtype(self, food_type: str) -> List[Tuple[str or float]]:

        self.cmd.execute(
            f'''
            SELECT *
            FROM Foods
            WHERE food_type = '{food_type}'
            '''
        )

        return self.cmd.fetchall()

db_access: DbAccess = DbAccess()
print(db_access.foods_by_foodtype(food_type='FoodType.Breakfast'))