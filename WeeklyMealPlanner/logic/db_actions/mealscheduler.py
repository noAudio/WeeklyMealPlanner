from calendar import monthrange
from random import randint
from typing import Any, Dict, List, Tuple
from mfdbaccess import MonthFormatDatabaseAccess
import datetime


class MealScheduler(MonthFormatDatabaseAccess):
    '''
        Creates a randomized timetable from the list of foods in the database based on a given month and year.
    '''
    _month_str: str
    _month: int
    _year: int
    _days: int
    _suppers: List[Tuple[str or float]]
    _breakfasts: List[Tuple[str or float]]

    def __init__(self, month: str, year: int) -> None:
        self.initial_setup(month=month, year=year)

    def initial_setup(self, month: str, year: int) -> None:
        self._month_str = month
        self._month = datetime.datetime.strptime(self._month_str[:3], '%b').month
        self._year = year
        self._days = monthrange(self._year, self._month)[1]
        self._suppers = self.foods_by_foodtype('FoodType.Supper')
        self._breakfasts = self.foods_by_foodtype('FoodType.Breakfast')
        pass

    def randomize_schedule(self) -> str:
        '''
         Create a list of random food combinations and pass them into a month table.
        '''
        breakfast_primaries: List[Tuple[str or float]] = self._sort_by_class(foods=self._breakfasts, foodclass='FoodClass.Primary')
        breakfast_secondaries: List[Tuple[str or float]] = self._sort_by_class(foods=self._breakfasts, foodclass='FoodClass.Secondary')
        supper_primaries: List[Tuple[str or float]] = self._sort_by_class(foods=self._suppers, foodclass='FoodClass.Primary')
        supper_secondaries: List[Tuple[str or float]] = self._sort_by_class(foods=self._suppers, foodclass='FoodClass.Secondary')
        date: int = 1

        status = self.create_month(month=self._month_str, year=self._year)

        if 'Error' in status:
            return status
        else:
            while date <= self._days:
                breakfast_primary = self._random_food(foods=breakfast_primaries)
                breakfast_secondary = self._random_food(foods=breakfast_secondaries)
                supper_primary = self._random_food(foods=supper_primaries)
                if supper_primary[0] == "'Spaghetti'":
                    supper_secondary = ["'Potatoes'", 40]
                else:
                    supper_secondary = self._random_food(foods=supper_secondaries)

                meal: Dict[str, Any] = {
                    'date': date,
                    'day': f"'{self._what_day(str(date), month=str(self._month), year=str(self._year))}'",
                    'breakfast_primary': f"{breakfast_primary[0]}",
                    'breakfast_secondary': f"{breakfast_secondary[0]}",
                    'breakfast_price': breakfast_primary[1] + breakfast_secondary[1],
                    'supper_primary': f"{supper_primary[0]}",
                    'supper_secondary': f"{supper_secondary[0]}",
                    'supper_price': supper_primary[1] + supper_secondary[1],
                    'day_price': breakfast_primary[1] + breakfast_secondary[1] + supper_primary[1] + supper_secondary[1] + 19.5,
                }

                date += 1
                
                status = self.add_food_to_month(meal=meal, month=self._month_str, year=self._year)
                if 'Error' in status:
                    break

            return status

    def _sort_by_class(self, foods: List[Tuple[str or float]], foodclass: str) -> List[Tuple[str or float]]:
        '''
            Sort foods by the specified food class (foodclass).
        '''
        sorted_foods: List[Tuple[str or float]] = []
        for food in foods:
            if food[3] == foodclass:
                sorted_foods.append(food)

        return sorted_foods

    def _random_food(self, foods: List[Tuple[str or float]]) -> List[Any]:
        '''
            Picks a random food from a list of foods and returns the food name and price in a list.
        '''
        food: Tuple[str or float] = foods[randint(0, len(foods) - 1)]
        return [f"'{food[1]}'", food[4]]

    def _what_day(self, day: str, month: str, year: str) -> str:
        '''
        Pass in a specific date and you will get its corresponding day e.g 04/11/2020 will return Wednesday.
        '''
        return datetime.date(int(year), int(month), int(day)).strftime('%A')
