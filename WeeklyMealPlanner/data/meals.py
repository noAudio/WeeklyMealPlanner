

class Meal:
    def __init__(self, combo_id: str, main_meal: str, supplementary_meal: str, combo_price: int) -> None:
        self.combo_id = combo_id
        self.main_meal = main_meal
        self.supplementary_meal = supplementary_meal
        self.combo_price = combo_price