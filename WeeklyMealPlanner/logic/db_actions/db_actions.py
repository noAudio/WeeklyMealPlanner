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
        self._commit_disconnect_db()

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
        Format will be:
            INSERT INTO table_name (headers)
            VALUES (values)
        '''
        self._table_name = table_name
        self._headers = ", ".join(str(header) for header in headers)
        self._values = ", ".join(str(value) for value in values)
        status: str = self.create_table(table_name=self._table_name, headers=headers)
        if 'Error' in status:
            return status
        try:
            self._execute(
                f'''
                INSERT INTO {self._table_name} ({self._headers})
                VALUES ({self._values})
                '''
            )
            return f'Successfully updated {self._table_name}'
        except OperationalError as e:
            return f'Error: {e}. Unable to update entry!'

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
        return record

class DbAccess(DBCommand):
    table_name: str

    def create_month(self, month: str, year: int) -> str:
        headers: List[str] = ['date INTEGER PRIMARY KEY',
                        'day VARCHAR',
                        'breakfast_primary VARCHAR',
                        'breakfast_secondary VARCHAR',
                        'breakfast_price FLOAT',
                        'supper_primary VARCHAR',
                        'supper_secondary VARCHAR',
                        'supper_price FLOAT',
                        'day_price FLOAT',
        ]
        return self.create_table(table_name=f'{month}_{year}', headers=headers)

    def delete_month(self, month: str, year: int) -> str:
        return self.drop_table(table_name=f'{month}_{year}')

    def add_food_to_month(self, meal: Dict[str, Any], month: str, year: int):
        '''
        Add an entry for daily meals to the pecific month's table. Pass in a meal, the desired month and year.
        '''
        headers: List[str] = ['date', 'day', 'breakfast_primary', 'breakfast_secondary', 'breakfast_price', 'supper_primary', 'supper_secondary', 'supper_price', 'day_price']
        values: List[str] = [f'{meal["date"]}', f'{meal["day"]}', f'{meal["breakfast_primary"]}', f'{meal["breakfast_secondary"]}', f'{meal["breakfast_price"]}', f'{meal["supper_primary"]}', f'{meal["supper_secondary"]}', f'{meal["supper_price"]}', f'{meal["day_price"]}',]
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
        values: List[Any] = [f'{food["id"]}', f'{food["name"]}', f'{food["food_type"]}', f'{food["food_class"]}', f'{food["price"]}']
        return str(self.update_table(table_name='Foods', headers=headers, values=values))

    def delete_food(self, id: str, name: str) -> str:
        '''
        Delete a food from the db.
        Accepts the name and id of the food to be deleted.
        '''
        status: str = self.delete_entry(table_name='Foods', header='id', value=id)
        if 'Success' in status:
            return f'Succesfully deleted {name}.'
        else:
            return status

    def edit_food(self, id: str, food: Dict[str, str or int]) -> str:
        '''
        Edit a food in the db.
        Accepts the id of the food to be deleted and a dictionary of the new food values.
        '''
        return self.edit_entry(table_name='Foods', primary_key="id", primary_key_value=f'{id}', **food)

    def foods_by_foodtype(self, food_type: str) -> List[Tuple[str or float]]:
        '''
        Find records based on a specified food type.
        '''
        return self.filter_records(table_name='Foods', header='food_type', value=food_type)

    def specified_day_meals(self, date: int, month: str, year: int) -> Tuple[str or float]:
        '''
        Find records based on a given date.
        '''
        return self.find_record(table_name=f'{month}_{year}', header='date', value=str(date))

    def _what_day(self, day: str, month: str, year: str) -> str:
        '''
        Pass in a specific date and you will get its corresponding day e.g 04/11/2020 will return Wednesday.
        '''
        return datetime.date(int(year), int(month), int(day)).strftime('%A')


december_schedule: DbAccess = DbAccess()
month: str = 'December'
year: int = 2020

# TODO: TEST 1: Create month
# print(december_schedule.create_month(month=month, year=year))

# TODO: TEST 2: Delete month
# print(december_schedule.delete_month(month=month, year=year))

# TODO: TEST 3: Add food to month
# food: Dict[str, Any] = {
#     "id": "'f99'",
#     "name": "'KDF'",
#     "food_type": "'Foodtype.breakfast'",
#     "food_class": "'FoodClass.Primary'",
#     "price": 40,
# }
# print(december_schedule.add_food(food=food))

# TODO: TEST 4: Add food to month
# TODO: TEST 5: Add new food
# TODO: TEST 6: Edit food
# new_food: Dict[str, Any] = {
#     "id": "'f99'",
#     "name": "'Greengrams'",
#     "food_type": "'Foodtype.Supper'",
#     "food_class": "'FoodClass.Secondary'",
#     "price": 50,
# }
# print(december_schedule.edit_food(id="'f88'", food=new_food))

# TODO: TEST 7: Delete food
# TODO: TEST 8: Filter foods
# TODO: TEST 9: Find specific meal by day





# db_access: DbAccess = DbAccess()
# suppers: List[Tuple[str or float]] = db_access.foods_by_foodtype(food_type='FoodType.Supper')
# breakfasts: List[Tuple[str or float]] = db_access.foods_by_foodtype(food_type='FoodType.Breakfast')

# def sort_by_class(foods: List[Tuple[str or float]], food_class: str) -> List[Tuple[str or float]]:
#     sorted_foods: List[Tuple[str or float]] = []
#     for food in foods:
#         if food[3] == food_class:
#             sorted_foods.append(food)
#     return sorted_foods
# breakfast_primaries: List[Tuple[str or float]] = sort_by_class(breakfasts, 'FoodClass.Primary')
# breakfast_secondaries: List[Tuple[str or float]] = sort_by_class(breakfasts, 'FoodClass.Secondary')
# supper_primaries: List[Tuple[str or float]] = sort_by_class(suppers, 'FoodClass.Primary')
# supper_secondaries: List[Tuple[str or float]] = sort_by_class(suppers, 'FoodClass.Secondary')

# def random_food(list: List[Tuple[str or float]]) -> List[Any]:
#     food: Tuple[str or float] = list[randint(0, len(list) - 1)]
#     food_name: str = food[1]
#     food_price: float = food[4]
#     return [food_name, food_price]

# total_days: int = 30
# date: int = 1

# month = '11'
# year = '2020'
# def what_day(day: str, month: str, year: str) -> str:
#     return datetime.date(int(year), int(month), int(day)).strftime('%A')

# while date <= total_days:
#     breakfast_primary = random_food(breakfast_primaries)
#     breakfast_secondary = random_food(breakfast_secondaries)
#     supper_primary = random_food(supper_primaries)
#     supper_secondary = random_food(supper_secondaries)


#     meal: Dict[str, Any] = {
#         'date': date,
#         'day': what_day(str(date), '11', '2020'),
#         'breakfast_primary': breakfast_primary[0],
#         'breakfast_secondary': breakfast_secondary[0],
#         'breakfast_price': breakfast_primary[1] + breakfast_secondary[1],
#         'supper_primary': supper_primary[0],
#         'supper_secondary': supper_secondary[0],
#         'supper_price': supper_primary[1] + supper_secondary[1],
#         'day_price': breakfast_primary[1] + breakfast_secondary[1] + supper_primary[1] + supper_secondary[1],
#     }
#     db_access.add_food_to_month(meal=meal, month='November', year=2020)
#     date += 1


#%%
# from typing import List
# h_list: List[str] = ['date INTEGER PRIMARY KEY', 'day VARCHAR', 'breakfast_primary VARCHAR', 'breakfast_secondary VARCHAR', 'breakfast_price FLOAT', 'supper_primary VARCHAR', 'supper_secondary VARCHAR', 'supper_price FLOAT', 'day_price FLOAT',]
# print(", ".join(str(header) for header in h_list))
#%%