from WeeklyMealPlanner.data.meal import Meal


class Day:
    breakfast: Meal
    supper: Meal

    def __init__(self, breakfast: Meal, supper: Meal) -> None:
        self.breakfast = breakfast
        self.supper = supper

    def daily_cost(self) -> float:
        return self.breakfast.meal_price() + self.supper.meal_price()