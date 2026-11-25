"""Inventory Management System, PS 21."""
from decimal import Decimal, InvalidOperation

LOW_STOCK_LIMIT = 5
inventory = {}
next_id = 1101

def parse_quantity(value):
    try:
        quantity = int(value)
        return quantity if quantity >= 0 else None
    except ValueError:
        return None

def parse_price(value):
    try:
        price = Decimal(value)
        return price if price.is_finite() and price >= 0 else None
    except InvalidOperation:
        return None

def format_amount(amount):
    text = format(amount, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text

def save_item(item_id, name, adding):
    quantity = parse_quantity(input("Quantity: " if adding else "New quantity: ").strip())
    price = parse_price(input("Price: " if adding else "New price: ").strip())
    if not name:
        error = "Name cannot be empty."
    elif quantity is None:
        error = "Invalid quantity. Quantity must be a non-negative whole number."
    elif price is None:
        error = "Invalid price. Price must be a non-negative number."
    else:
        if adding:
            inventory[item_id] = {"name": name, "quantity": quantity, "price": price}
            print(f"Item added | ID: {item_id} | {name} | Qty: {quantity} | Price: {format_amount(price)}")
        else:
            inventory[item_id].update(quantity=quantity, price=price)
            print(f"Item ID {item_id} updated.")
        if quantity < LOW_STOCK_LIMIT:
            print(f"Low stock alert: {name} ({quantity})")
        return True
    print(error, "Item not added." if adding else "Item not updated.")
    return False

def add_item():
    global next_id
    name = input("Name: ").strip()
    if save_item(next_id, name, adding=True):
        next_id += 1

def read_item_id(action):
    item_id = parse_quantity(input(f"Enter Item ID to {action}: ").strip())
    if item_id is None:
        print("Invalid item ID.")
    elif item_id in inventory:
        return item_id
    else:
        print(f"Item ID {item_id} not found")
    return None

def update_item():
    item_id = read_item_id("update")
    if item_id is not None:
        save_item(item_id, inventory[item_id]["name"], adding=False)

def delete_item():
    item_id = read_item_id("delete")
    if item_id is not None:
        item = inventory.pop(item_id)
        print(f"Item '{item['name']}' deleted. Items left: {len(inventory)}")

def display_items(items, empty_message=None):
    rows = list(items)
    if not rows and empty_message:
        print(empty_message)
        return
    width = max([4] + [len(item["name"]) for _, item in rows])
    print(f'{"ID":<8} {"NAME":<{width}} {"QTY":>8} {"PRICE":>12}')
    for item_id, item in rows:
        price = format_amount(item["price"])
        print(f'{item_id:<8} {item["name"]:<{width}} {item["quantity"]:>8} {price:>12}')

def view_items():
    display_items(inventory.items(), "Inventory is empty.")

def search_items():
    query = input("Enter item name or ID: ").strip().casefold()
    if not query:
        print("Enter a name or ID to search.")
        return
    matches = [(key, item) for key, item in inventory.items()
               if query == str(key) or query in item["name"].casefold()]
    display_items(matches, "No matching items.")

def show_total_value():
    total = sum(item["quantity"] * item["price"] for item in inventory.values())
    print(f"Total stock value: {format_amount(total)}")

def show_low_stock():
    low = [item for item in inventory.values() if item["quantity"] < LOW_STOCK_LIMIT]
    if low:
        print(f"Low stock (below {LOW_STOCK_LIMIT}):")
        for item in low:
            print(f'{item["name"]} | Qty: {item["quantity"]}')
    else:
        print("No low-stock items.")

OPTIONS = {
    "1": ("Add item", add_item), "2": ("View items", view_items),
    "3": ("Update item", update_item), "4": ("Delete item", delete_item),
    "5": ("Total stock value", show_total_value), "6": ("Low-stock report", show_low_stock),
    "7": ("Search items", search_items),
}
menu_lines = [f"{key}. {label}" for key, (label, _) in OPTIONS.items()]
MENU = "\n".join(["", "Inventory Management System (PS 21)", *menu_lines, "8. Exit"])

def main():
    try:
        while True:
            print(MENU)
            choice = input("Menu option: ").strip()
            if choice == "8":
                break
            if choice in OPTIONS:
                _, action = OPTIONS[choice]
                action()
            else:
                print("Please choose an option from 1 to 8.")
    except (EOFError, KeyboardInterrupt):
        print()
    print("Goodbye!")

if __name__ == "__main__":
    main()
