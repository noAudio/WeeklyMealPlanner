# TODO1: Access this week's worth of meals
# TODO2: Reroll by deleting a month and randomizing it again

from mealscheduler import MealScheduler
# from WeeklyMealPlanner.logic.db_actions.mealscheduler import MealScheduler
from typing import Any, List
import datetime


class UserActions(MealScheduler):
    weekdays: List[str] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    index: int
    table_name: str
    _month: str
    _year: int
    _date: int

    def __init__(self, date: int, month: str, year: int) -> None:
        self._month = month
        self._year = year
        self._date = date
        self.index = datetime.date(int(year), datetime.datetime.strptime(self._month, '%B').month, int(date)).weekday()
        self.table_name = f'{self._month}_{year}'

    def this_week(self) -> List[Any]:
        '''
        Get a list of meals for the previous day, current day and the next 5 days.
        '''
        days: List[int] = [self._date - 1, self._date, self._date + 1, self._date + 2, self._date + 3, self._date + 4, self._date + 5]
        current_meals: List[str] = []

        for each_day in days:
            current_meals.append(self.specified_day_meals(date=each_day, month=self._month, year=self._year))        

        return current_meals
    
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

