from WeeklyMealPlanner.logic.data.foods import Food

'''
    Attributes:
        combo_id: str (unique id for food combinations)
        primary_food: Food (a primary food)
        secondary_food: Food (a secondary food)
        _condiments_price: float (a constant price for condiments)
    Methods:
        meal_price() -> float (calculates total price of the meal)
'''
class Meal:
    combo_id: str
    primary_food: Food
    secondary_food: Food
    _condiments_price: float = 19.5

    def __init__(self, combo_id: str, primary_food: Food, secondary_food: Food) -> None:
        self.combo_id = combo_id
        self.primary_food = primary_food
        self.secondary_food = secondary_food
    
    def meal_price(self) -> float:
        return self.primary_food.price + self.secondary_food.price + self._condiments_price

    