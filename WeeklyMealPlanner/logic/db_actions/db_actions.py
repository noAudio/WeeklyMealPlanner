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
        self.__connect_to_db__()
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
        except sqlite3.IntegrityError as e:
            error: str = f'Error: "{e}". Table already exists!'
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

    def add_food_to_month(self, meal: Dict[str, Any], month: str, year: int) -> str:
        '''
        '''
        self.__connect_to_db__()
        create: str = self.create_month(month=month, year=year)
        if 'Error' in create:
            return create
        else:
            self.cmd.execute(
                f'''
                INSERT INTO {month}_{year} (date, day, breakfast_primary, breakfast_secondary, breakfast_price, supper_primary, supper_secondary, supper_price, day_price)
                VALUES ('{meal['date']}', '{meal['day']}', '{meal['breakfast_primary']}', '{meal['breakfast_secondary']}', '{meal['breakfast_price']}', '{meal['supper_primary']}', '{meal['supper_secondary']}', '{meal['supper_price']}', '{meal['day_price']}')
                '''
            )
            self.connection.commit()
            self.connection.close()
            return ''
        
    def add_food(self, food: Dict[str, Any]) -> str:
        '''
        Add a food to the db.
        Accepts a dictionary with food properties which are then added as an entry.
        '''
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
        self.__connect_to_db__()
        self.cmd.execute(
            f'''
            SELECT *
            FROM Foods
            WHERE food_type = '{food_type}'
            '''
        )
        foods: List[Tuple[str or float]] = self.cmd.fetchall()
        self.connection.commit()
        self.connection.close()
        return foods
    
    def specified_day_meals(self, date: int, month: str, year: int) -> Tuple[str or float]:
        '''
        Find records based on a given date.
        '''
        self.table_name = f'{month}_{year}'
        self.__connect_to_db__()
        self.cmd.execute(
            f'''
            SELECT *
            FROM {self.table_name}
            WHERE date = '{date}'
            '''
        )
        meal: Tuple[str or float] = self.cmd.fetchone()
        self.connection.commit()
        self.connection.close()
        return meal

db_access: DbAccess = DbAccess()
suppers: List[Tuple[str or float]] = db_access.foods_by_foodtype(food_type='FoodType.Supper')
breakfasts: List[Tuple[str or float]] = db_access.foods_by_foodtype(food_type='FoodType.Breakfast')

from random import randint
def sort_by_class(foods: List[Tuple[str or float]], food_class: str) -> List[Tuple[str or float]]:
    sorted_foods: List[Tuple[str or float]] = []
    for food in foods:
        if food[3] == food_class:
            sorted_foods.append(food)
    return sorted_foods
breakfast_primaries: List[Tuple[str or float]] = sort_by_class(breakfasts, 'FoodClass.Primary')
breakfast_secondaries: List[Tuple[str or float]] = sort_by_class(breakfasts, 'FoodClass.Secondary')
supper_primaries: List[Tuple[str or float]] = sort_by_class(suppers, 'FoodClass.Primary')
supper_secondaries: List[Tuple[str or float]] = sort_by_class(suppers, 'FoodClass.Secondary')

def random_food(list: List[Tuple[str or float]]) -> List[Any]:
    food: Tuple[str or float] = list[randint(0, len(list) - 1)]
    food_name: str = food[1]
    food_price: float = food[4]
    return [food_name, food_price]

total_days: int = 30
date: int = 1

while date <= total_days:
    breakfast_primary = random_food(breakfast_primaries)
    breakfast_secondary = random_food(breakfast_secondaries)
    supper_primary = random_food(supper_primaries)
    supper_secondary = random_food(supper_secondaries)
    meal: Dict[str, Any] = {
        'date': date,
        'day': 'Monday',
        'breakfast_primary': breakfast_primary[0],
        'breakfast_secondary': breakfast_secondary[0],
        'breakfast_price': breakfast_primary[1] + breakfast_secondary[1],
        'supper_primary': supper_primary[0],
        'supper_secondary': supper_secondary[0],
        'supper_price': supper_primary[1] + supper_secondary[1],
        'day_price': breakfast_primary[1] + breakfast_secondary[1] + supper_primary[1] + supper_secondary[1],
    }
    msg: str = db_access.add_food_to_month(meal=meal, month='October', year=2020)
    if 'Error' in msg:
        print(msg, '\nBreaking operation')
        break
    date += 1

print(db_access.specified_day_meals(date=12, month='October', year=2020))