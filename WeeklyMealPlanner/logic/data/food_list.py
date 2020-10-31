from WeeklyMealPlanner.logic.data.foods import Food, FoodType, FoodClass
from typing import Any, Dict, List

all_foods: List[Dict[str, Any]] = [
    {
        'name': 'Rice',
        'food_type': FoodType.Supper,
        'food_class': FoodClass.Primary,
        'price': 50,
    },
    {
        'name': 'Chapati',
        'food_type': FoodType.Supper,
        'food_class': FoodClass.Primary,
        'price': 80,
    },
    {
        'name': 'Spaghetti',
        'food_type': FoodType.Supper,
        'food_class': FoodClass.Primary,
        'price': 50,
    },
    {
        'name': 'Potatoes',
        'food_type': FoodType.Supper,
        'food_class': FoodClass.Secondary,
        'price': 40,
    },
    {
        'name': 'Ndengu',
        'food_type': FoodType.Supper,
        'food_class': FoodClass.Secondary,
        'price': 40,
    },
    {
        'name': 'Githeri',
        'food_type': FoodType.Supper,
        'food_class': FoodClass.Secondary,
        'price': 40,
    },
    {
        'name': 'Mbaazi',
        'food_type': FoodType.Supper,
        'food_class': FoodClass.Secondary,
        'price': 40,
    },
    {
        'name': 'Bread',
        'food_type': FoodType.Breakfast,
        'food_class': FoodClass.Primary,
        'price': 50,
    },
    {
        'name': 'Eggs',
        'food_type': FoodType.Breakfast,
        'food_class': FoodClass.Secondary,
        'price': 44,
    },
    {
        'name': 'Mandazi',
        'food_type': FoodType.Breakfast,
        'food_class': FoodClass.Primary,
        'price': 40,
    },
]

def foods() -> List[Food]:
    foods: List[Food] = []
    for food in all_foods:
        foods.append(Food(name=food['name'], food_type=food['food_type'], food_class=food['food_class'], price=food['price']))
    return foods