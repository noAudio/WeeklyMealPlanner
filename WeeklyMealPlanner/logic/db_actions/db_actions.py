
from mealscheduler import MealScheduler


mealscheduler: MealScheduler = MealScheduler(month='January', year=2023)
print(mealscheduler.randomize_schedule())