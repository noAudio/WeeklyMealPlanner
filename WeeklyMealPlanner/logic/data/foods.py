from enum import Enum

class FoodType(Enum):
    Breakfast = 1
    Supper = 2

class FoodClass(Enum):
    Primary = 1
    Secondary = 2

class Food:
    name: str
    food_type: FoodType
    food_class: FoodClass
    price: int

    def __init__(self, name: str, food_type: FoodType, food_class: FoodClass, price: int) -> None:
        self.name = name
        self.food_type = food_type
        self.food_class = food_class
        self.price = price