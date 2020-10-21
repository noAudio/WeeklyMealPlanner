from meal import Meal

class Day:
    breakfast: Meal
    supper: Meal
    daily_cost: int = 0

    def __init__(self, breakfast: Meal, supper: Meal) -> None:
        self.breakfast = breakfast
        self.supper = supper

    def daily_price(self) -> int:
        
        
        return 0
