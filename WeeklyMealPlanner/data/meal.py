

class Meal:
    combo_id: str = ''
    combo_price: int = 0

    def __init__(self, combo_id: str, combo_price: int) -> None:
        self.combo_id = combo_id
        self.combo_price = combo_price