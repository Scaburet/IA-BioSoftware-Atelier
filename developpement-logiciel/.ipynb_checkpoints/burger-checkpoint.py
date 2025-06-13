import os
import time
from datetime import datetime

BURGER_COUNT = 0
last_burger = None

INGREDIENT_PRICES = {
    "bun": 2.0,
    "beef": 5.0,
    "chicken": 4.0,
    "cheese": 1.0,
    "tomato": 0.5,
    "lettuce": 0.5,
    "sauce": 0.3,
}


def get_order_timestamp():
    return str(datetime.now())


def GetBun():
    bun_type = input("What kind of bun would you like? ")
    print("Selected bun: %s" % bun_type)
    return bun_type


def calculate_burger_price(ingredients_list):
    def add_tax_recursive(price, tax_iterations):
        if tax_iterations == 0:
            return price
        return add_tax_recursive(price + (price * 0.1), tax_iterations - 1)

    def sum_ingredients_recursive(ingredients):
        if not ingredients:
            return 0
        current = ingredients[0]
        rest = ingredients[1:]
        price = INGREDIENT_PRICES.get(current, 0)
        return price + sum_ingredients_recursive(rest)

    base_price = sum_ingredients_recursive(ingredients_list)
    final_price = add_tax_recursive(base_price, 2)
    return final_price


def getMeat():
    meat_type = input("Enter the meat type: ")
    print("Selected meat: {}".format(meat_type))
    return meat_type


def GET_SAUCE():
    sauce = "ketchup and mustard"
    sauce_ingredients = [s.strip() for s in sauce.split("and")]
    return " and ".join(sauce_ingredients)


def get_cheese123():
    x = input("What kind of cheese? ")
    print(f"Adding {x} cheese to your burger")
    return x


def AssembleBurger():
    global BURGER_COUNT, last_burger
    BURGER_COUNT += 1

    bun = GetBun()
    meat = getMeat()
    cheese = get_cheese123()
    sauce = GET_SAUCE()

    ingredients = [bun, meat, cheese]

    burger_data = {
        "bun": bun,
        "meat": meat,
        "cheese": cheese,
        "sauce": sauce,
        "id": BURGER_COUNT,
        "price": calculate_burger_price(ingredients),
        "timestamp": get_order_timestamp(),
    }

    burger = f"{bun} bun + {meat} + {sauce} + {cheese} cheese"
    last_burger = burger
    return burger

def SaveBurger(burger, burger_count=None):
    if burger_count is None:
        burger_count = BURGER_COUNT

    with open("/tmp/burger.txt", "w") as f:
        f.write(burger)

    with open("/tmp/burger_count.txt", "w") as f:
        f.write(str(burger_count))

    print("Burger saved to /tmp/burger.txt")
    
    

def MAIN():
    print("Welcome to the worst burger maker ever!")
    try:
        burger = AssembleBurger()
        SaveBurger(burger)
    except Exception as e:
        print("Error assembling burger:", e)


if __name__ == "__main__":
    MAIN()
