# from WeeklyMealPlanner.logic.data.foods import FoodClass, FoodType
from sqlite3 import connect, OperationalError, IntegrityError
from sqlite3.dbapi2 import Connection, Cursor
from typing import Any, Dict, List, Tuple
from random import randint
import datetime

class DBConnection:
    '''
    Establish connection to database.
    Also allows database commit and disconnection via _commit_disconnect_db().
    '''
    connection: Connection
    _db: str = 'foods.db'

    def __init__(self) -> None:
        '''
        Access the db to read, add, update, delete and/or remove tables and table entries
        '''
        self._connect_db()

    def _connect_db(self) -> None:
        '''
        Instantiate a connection to the database.
        '''
        self.connection: Connection = connect(self._db)
        self.cmd: Cursor = self.connection.cursor()
    
    def _commit_disconnect_db(self) -> None:
        '''
        Commit changes and close database connection.
        '''
        self.connection.commit()
        self.connection.close()

class DBCommand(DBConnection):
    '''
    Handles command execution in the database.
    '''
    cmd: Cursor
    _table_name: str
    _headers: List[str]
    _values: List[str]

    
    def __init__(self) -> None:
        self._connect_db()
    
    def _execute(self, command: str) -> None:
        '''
        Pass in a command to be executed in the database.
        '''
        self.cmd.execute(command)
        self._commit_disconnect_db()
    
    def create_table(self, table_name: str) -> str:
        ''''
        Create a new table for the month in the db.
        Pass in a name for the table.
        '''
        self._table_name = table_name
        try:
            self._execute(
                f'''
                    CREATE TABLE IF NOT EXISTS {self._table_name} (
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
            return f'Success! Table "{self._table_name}" has been deleted.'
        except OperationalError as e:
            return f'Error: "{e}". Unable to perform delete operation!'
    
    def update_table(self, table_name: str, headers: List[str], values: List[str]) -> Any:
        '''
        Update the contents of a table. Pass in the command with headers and values.
        '''
        self._table_name = table_name
        self._headers = headers
        self._values = values
        status: str = self.create_table(table_name=self._table_name)
        if 'Error' in status:
            return status
        self._execute(
            f'''
            INSERT INTO {self._table_name} ({self._headers})
            VALUES ({self._values})
            '''
        )

class DbAccess(DBCommand):
    table_name: str

    def __init__(self) -> None:
        pass

    def create_month(self, month: str, year: int) -> str:
        return self.create_table(table_name=f'{month}_{year}')
    
    def delete_month(self, month: str, year: int) -> str:
        return self.drop_table(table_name=f'{month}_{year}')

    def add_food_to_month(self, meal: Dict[str, Any], month: str, year: int):
        '''
        Add an entry for daily meals to the pecific month's table. Pass in a meal, the desired month and year.
        '''
        headers: List[str] = ['date', 'day', 'breakfast_primary', 'breakfast_secondary', 'breakfast_price', 'supper_primary', 'supper_secondary', 'supper_price', 'day_price']
        values: List[str] = ['{meal["date"]}', '{meal["day"]}', '{meal["breakfast_primary"]}', '{meal["breakfast_secondary"]}', '{meal["breakfast_price"]}', '{meal["supper_primary"]}', '{meal["supper_secondary"]}', '{meal["supper_price"]}', '{meal["day_price"]}',]
        return str(self.update_table(table_name=f'{month}_{year}', headers=headers, values=values))
    
    def randomize_schedule(self, date: str) -> None:
        '''
         Create a list of random food combinations and pass them into a month table.
        '''
        # TODO: 1.Run a check for the month passed in as an argument
        # day: str = self._what_day(month=month, year=year)
        # TODO: 2.Use a while loop with the number of days in the specified month
        # TODO: 3.Read the FOOD table and sort foods by categories
        # TODO: 4.Randomise sorted foods and pass into a list
        # TODO: 5.Pass data off into a table.
        pass
        
    def add_food(self, food: Dict[str, Any]) -> str:
        '''
        Add a food to the db.
        Accepts a dictionary with food properties which are then added as an entry.
        '''
        headers: List[str] = ['id', 'name', 'food_type', 'food_class', 'price']
        values: List[Any] = ['{food["id"]}', '{food["name"]}', '{food["food_type"]}', '{food["food_class"]}', {food["price"]}]
        try:
            return str(self.update_table(table_name='Foods', headers=headers, values=values))
        except OperationalError as e:
            return f'Error "{e}". Unable to update entry!'
        
    def delete_food(self, id: str, name: str) -> str:
        '''
        Delete a food from the db.
        Accepts the name and id of the food to be deleted.
        '''
        self._execute(
            f'''
            DELETE FROM Foods
            WHERE id = '{id}'
            '''
        )
        return f'Succesfully deleted {name}.'
    
    def edit_food(self, id: str, food: Any) -> str:
        '''
        Edit a food in the db.
        Accepts the id of the food to be deleted and a dictionary of the new food values.
        '''
        self._execute(
            f'''
            UPDATE Foods
            SET name = '{food["name"]}', food_type = '{food["food_type"]}', food_class = '{food["food_class"]}', price = '{food["price"]}'
            WHERE id = '{id}'
            '''
        )
        return f'Succesfully edited food.'
    
    def foods_by_foodtype(self, food_type: str) -> List[Tuple[str or float]]:
        '''
        Find records based on a specified food type.
        '''
        self._connect_db()
        self.cmd.execute(
            f'''
            SELECT *
            FROM Foods
            WHERE food_type = '{food_type}'
            '''
        )
        foods: List[Tuple[str or float]] = self.cmd.fetchall()
        self._commit_disconnect_db()
        return foods
    
    def specified_day_meals(self, date: int, month: str, year: int) -> Tuple[str or float]:
        '''
        Find records based on a given date.
        '''
        self.table_name = f'{month}_{year}'
        self._connect_db()
        self.cmd.execute(
            f'''
            SELECT *
            FROM {self.table_name}
            WHERE date = '{date}'
            '''
        )
        meal: Tuple[str or float] = self.cmd.fetchone()
        self._commit_disconnect_db()
        return meal
    def _what_day(self, day: str, month: str, year: str) -> str:
        '''
        Pass in a specific date and you will get its corresponding day e.g 04/11/2020 will return Wednesday.
        '''
        return datetime.date(int(year), int(month), int(day)).strftime('%A')




db_access: DbAccess = DbAccess()
suppers: List[Tuple[str or float]] = db_access.foods_by_foodtype(food_type='FoodType.Supper')
breakfasts: List[Tuple[str or float]] = db_access.foods_by_foodtype(food_type='FoodType.Breakfast')

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

month = '11'
year = '2020'
def what_day(day: str, month: str, year: str) -> str:
    return datetime.date(int(year), int(month), int(day)).strftime('%A')

while date <= total_days:
    breakfast_primary = random_food(breakfast_primaries)
    breakfast_secondary = random_food(breakfast_secondaries)
    supper_primary = random_food(supper_primaries)
    supper_secondary = random_food(supper_secondaries)


    meal: Dict[str, Any] = {
        'date': date,
        'day': what_day(str(date), '11', '2020'),
        'breakfast_primary': breakfast_primary[0],
        'breakfast_secondary': breakfast_secondary[0],
        'breakfast_price': breakfast_primary[1] + breakfast_secondary[1],
        'supper_primary': supper_primary[0],
        'supper_secondary': supper_secondary[0],
        'supper_price': supper_primary[1] + supper_secondary[1],
        'day_price': breakfast_primary[1] + breakfast_secondary[1] + supper_primary[1] + supper_secondary[1],
    }
    db_access.add_food_to_month(meal=meal, month='November', year=2020)
    date += 1
