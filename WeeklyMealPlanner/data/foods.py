from enum import Enum

class FoodType(Enum):
    Breakfast = 1
    Supper = 2

class Food:
    name: str
    food_type: FoodType
    price: int

    def __init__(self, name: str, food_type: FoodType, price: int) -> None:
        self.name = name
        self.food_type = food_type
        self.price = price