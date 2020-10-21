from enum import Enum

class FoodType(Enum):
    Breakfast = 1
    Supper = 2

class Food:
    name: str
    type: FoodType
    price: int