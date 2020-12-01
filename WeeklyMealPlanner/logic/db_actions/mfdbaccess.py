from typing import Any, Dict, List, Tuple
from dbcommand import DBCommand


class MonthFormatDatabaseAccess(DBCommand):
    '''
        Handles how data will be formatted and recorded into the database.
    '''
    table_name: str

    def create_month(self, month: str, year: int) -> str:
        '''
            Creates a table in the database for the specified month. Pass in month and year to create table name.
        '''
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
        '''
            Delete a specified month table from the database. Pass in month and year to create table name.
        '''
        return self.drop_table(table_name=f'{month}_{year}')

    def add_food_to_month(self, meal: Dict[str, Any], month: str, year: int):
        '''
        Add an entry for daily meals to the pecific month's table. Pass in a meal, the desired month and year.
        '''
        headers: List[str] = ['date', 'day', 'breakfast_primary', 'breakfast_secondary', 'breakfast_price', 'supper_primary', 'supper_secondary', 'supper_price', 'day_price']
        values: List[Any] = [f'{meal["date"]}', f'{meal["day"]}', f'{meal["breakfast_primary"]}', f'{meal["breakfast_secondary"]}', meal["breakfast_price"], f'{meal["supper_primary"]}', f'{meal["supper_secondary"]}', meal["supper_price"], meal["day_price"],]
        return str(self.update_table(table_name=f'{month}_{year}', headers=headers, values=values))

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
        status: Tuple[str] = self.find_record(table_name=f'{month}_{year}', header='date', value=str(date))
        if status != None:
            return status
        elif status == None:
            return ('Requested record does not exist.',)
        return status
