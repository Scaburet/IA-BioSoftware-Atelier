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


def get_bun():
    bun_type = input("What kind of bun would you like? ")
    print(f"Selected bun: {bun_type}")
    return bun_type


def get_meat():
    meat_type = input("Enter the meat type: ")
    print(f"Selected meat: {meat_type}")
    return meat_type


def get_sauce():
    sauce = "ketchup and mustard"
    sauce_ingredients = [s.strip() for s in sauce.split("and")]
    return " and ".join(sauce_ingredients)


def get_cheese():
    cheese_type = input("What kind of cheese? ")
    print(f"Adding {cheese_type} cheese to your burger")
    return cheese_type


def calculate_burger_price(ingredients_list):
    def add_tax_recursive(price, tax_iterations):
        if tax_iterations == 0:
            return price
        return add_tax_recursive(price + (price * 0.1), tax_iterations - 1)

    def sum_ingredients_recursive(ingredients):
        if not ingredients:
            return 0
        return INGREDIENT_PRICES.get(ingredients[0], 0) + sum_ingredients_recursive(ingredients[1:])

    base_price = sum_ingredients_recursive(ingredients_list)
    return add_tax_recursive(base_price, 2)


def assemble_burger():
    global BURGER_COUNT, last_burger
    BURGER_COUNT += 1

    bun = get_bun()
    meat = get_meat()
    cheese = get_cheese()
    sauce = get_sauce()

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


def save_burger(burger):
    with open("/tmp/burger.txt", "w") as f:
        f.write(burger)

    with open("/tmp/burger_count.txt", "w") as f:
        f.write(str(BURGER_COUNT))

    print("Burger saved to /tmp/burger.txt")


def main():
    print("Welcome to the worst burger maker ever!")
    try:
        burger = assemble_burger()
        save_burger(burger)
    except Exception as e:
        print("Error assembling burger:", e)


if __name__ == "__main__":
    main()
