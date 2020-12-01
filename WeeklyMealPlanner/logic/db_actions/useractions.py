# TODO1: Access this week's worth of meals
# TODO2: Reroll by deleting a month and randomizing it again

from mealscheduler import MealScheduler
from typing import Any, List
import datetime


class UserActions(MealScheduler):
    weekdays: List[str] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    index: int
    table_name: str
    _month: str
    _year: int

    def __init__(self, date: int, month: str, year: int) -> None:
        self._month = month
        self._year = year
        self.index = datetime.date(int(year), datetime.datetime.strptime(self._month, '%B').month, int(date)).weekday()
        self.table_name = f'{self._month}_{year}'

    def this_week(self) -> List[Any]:
        '''
        - while loop couonting down to zero to get previous days
        - while loop counting up to 6 to get the next available days
        - append all to form a list of numbers
        - for loop using list of numbers as dates to access the db and create a list of days with meals
        - return list of days
        '''

        return []
    
    def reroll_month(self) -> str:
        '''
        Deletes the specified month then randomizes a new schedule and recreates a new month with the new values.
        '''
        status: str = self.delete_month(month=self._month, year=self._year)
        if 'Error' in status:
            return status
        self.initial_setup(month=self._month, year=self._year)
        status = self.randomize_schedule()
        return status

useraction: UserActions = UserActions(1, 'January', 2023)
print(useraction.reroll_month())

#%%

# %%
