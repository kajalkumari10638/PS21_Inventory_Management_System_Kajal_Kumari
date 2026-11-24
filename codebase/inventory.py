"""Inventory Management System, project statement PS 21."""

from decimal import Decimal, InvalidOperation

LOW_STOCK_LIMIT = 5
inventory = {}
next_id = 1101


def parse_quantity(value):
    try:
        quantity = int(value)
    except ValueError:
        return None
    return quantity if quantity >= 0 else None


def parse_price(value):
    try:
        price = Decimal(value)
    except InvalidOperation:
        return None
    return price if price.is_finite() and price >= 0 else None


def format_amount(amount):
    text = format(amount, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def add_item():
    global next_id
    name = input("Name: ").strip()
    quantity = parse_quantity(input("Quantity: ").strip())
    price = parse_price(input("Price: ").strip())

    if not name:
        print("Name cannot be empty. Item not added.")
        return
    if quantity is None:
        print("Invalid quantity. Quantity must be a non-negative whole number. Item not added.")
        return
    if price is None:
        print("Invalid price. Price must be a non-negative number. Item not added.")
        return

    inventory[next_id] = {"name": name, "quantity": quantity, "price": price}
    print(f"Item added | ID: {next_id} | {name} | Qty: {quantity} | Price: {format_amount(price)}")
    if quantity < LOW_STOCK_LIMIT:
        print(f"Low stock alert: {name} ({quantity})")
    next_id += 1


def display_items(items):
    rows = list(items)
    name_width = max([4] + [len(item["name"]) for _, item in rows])
    print(f'{"ID":<8} {"NAME":<{name_width}} {"QTY":>8} {"PRICE":>12}')
    for item_id, item in rows:
        price = format_amount(item["price"])
        print(f'{item_id:<8} {item["name"]:<{name_width}} {item["quantity"]:>8} {price:>12}')


def view_items():
    if not inventory:
        print("Inventory is empty.")
        return
    display_items(inventory.items())


def read_item_id(action):
    raw_id = input(f"Enter Item ID to {action}: ").strip()
    item_id = parse_quantity(raw_id)
    if item_id is None:
        print("Invalid item ID.")
    elif item_id not in inventory:
        print(f"Item ID {item_id} not found")
        return None
    return item_id


def update_item():
    item_id = read_item_id("update")
    if item_id is None:
        return

    quantity = parse_quantity(input("New quantity: ").strip())
    price = parse_price(input("New price: ").strip())
    if quantity is None:
        print("Invalid quantity. Quantity must be a non-negative whole number. Item not updated.")
        return
    if price is None:
        print("Invalid price. Price must be a non-negative number. Item not updated.")
        return

    item = inventory[item_id]
    item.update(quantity=quantity, price=price)
    print(f"Item ID {item_id} updated.")
    if quantity < LOW_STOCK_LIMIT:
        print(f'Low stock alert: {item["name"]} ({quantity})')


def delete_item():
    item_id = read_item_id("delete")
    if item_id is not None:
        item = inventory.pop(item_id)
        print(f"Item '{item['name']}' deleted. Items left: {len(inventory)}")


def show_total_value():
    total = sum(item["quantity"] * item["price"] for item in inventory.values())
    print(f"Total stock value: {format_amount(total)}")


def show_low_stock():
    low_stock = [item for item in inventory.values() if item["quantity"] < LOW_STOCK_LIMIT]
    if not low_stock:
        print("No low-stock items.")
        return
    print(f"Low stock (below {LOW_STOCK_LIMIT}):")
    for item in low_stock:
        print(f'{item["name"]} | Qty: {item["quantity"]}')


def search_items():
    query = input("Enter item name or ID: ").strip().casefold()
    if not query:
        print("Enter a name or ID to search.")
        return

    matches = [
        (item_id, item)
        for item_id, item in inventory.items()
        if query == str(item_id) or query in item["name"].casefold()
    ]
    if matches:
        display_items(matches)
    else:
        print("No matching items.")


MENU = """\nInventory Management System (PS 21)
1. Add item
2. View items
3. Update item
4. Delete item
5. Total stock value
6. Low-stock report
7. Search items
8. Exit"""


def main():
    actions = {
        "1": add_item,
        "2": view_items,
        "3": update_item,
        "4": delete_item,
        "5": show_total_value,
        "6": show_low_stock,
        "7": search_items,
    }

    try:
        while True:
            print(MENU)
            choice = input("Menu option: ").strip()
            if choice == "8":
                break
            action = actions.get(choice)
            if action is None:
                print("Please choose an option from 1 to 8.")
            else:
                action()
    except (EOFError, KeyboardInterrupt):
        print()
    print("Goodbye!")


if __name__ == "__main__":
    main()
