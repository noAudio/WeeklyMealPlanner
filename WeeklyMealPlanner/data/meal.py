from WeeklyMealPlanner.data.foods import Food

class Meal:
    combo_id: str
    primary_food: Food
    secondary_food: Food
    _condiments_price: float = 19.5

    def __init__(self, combo_id: str) -> None:
        self.combo_id = combo_id
    
    def meal_price(self) -> float:
        return self.primary_food.price + self.secondary_food.price + self._condiments_price

    