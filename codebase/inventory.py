"""Inventory Management System, PS 21."""
from decimal import Decimal, InvalidOperation

inventory = {}
next_id = 1101
LOW_STOCK_LIMIT = 5

def number(text, kind=int):
    try:
        value = kind(text)
        if kind is Decimal and not value.is_finite():
            return None
        return value if value >= 0 else None
    except (ValueError, InvalidOperation):
        return None

def amount(value):
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text

def save_item(item_id, name, adding):
    quantity = number(input("Quantity: " if adding else "New quantity: ").strip())
    price = number(input("Price: " if adding else "New price: ").strip(), Decimal)
    failure = "Item not added." if adding else "Item not updated."
    if not name:
        print("Name cannot be empty.", failure)
    elif quantity is None:
        print("Invalid quantity. Quantity must be a non-negative whole number.", failure)
    elif price is None:
        print("Invalid price. Price must be a non-negative number.", failure)
    else:
        inventory[item_id] = {"name": name, "quantity": quantity, "price": price}
        if adding:
            print(f"Item added | ID: {item_id} | {name} | Qty: {quantity} | Price: {amount(price)}")
        else:
            print(f"Item ID {item_id} updated.")
        if quantity < LOW_STOCK_LIMIT:
            print(f"Low stock alert: {name} ({quantity})")

def add_item():
    global next_id
    save_item(next_id, input("Name: ").strip(), adding=True)
    if next_id in inventory:
        next_id += 1

def change_item(action):
    item_id = number(input(f"Enter Item ID to {action}: ").strip())
    if item_id not in inventory:
        print("Invalid item ID." if item_id is None else f"Item ID {item_id} not found")
    elif action == "update":
        save_item(item_id, inventory[item_id]["name"], adding=False)
    else:
        item = inventory.pop(item_id)
        print(f"Item '{item['name']}' deleted. Items left: {len(inventory)}")

def display_items(rows, empty_message):
    if not rows:
        print(empty_message)
        return
    width = max([4] + [len(item["name"]) for _, item in rows])
    print(f'{"ID":<8} {"NAME":<{width}} {"QTY":>8} {"PRICE":>12}')
    for item_id, item in rows:
        price = amount(item["price"])
        print(f'{item_id:<8} {item["name"]:<{width}} {item["quantity"]:>8} {price:>12}')

def search_items():
    query = input("Enter item name or ID: ").strip().casefold()
    if query:
        matches = [(key, item) for key, item in inventory.items()
                   if query == str(key) or query in item["name"].casefold()]
        display_items(matches, "No matching items.")
    else:
        print("Enter a name or ID to search.")

def show_low_stock():
    low = [item for item in inventory.values() if item["quantity"] < LOW_STOCK_LIMIT]
    print(f"Low stock (below {LOW_STOCK_LIMIT}):" if low else "No low-stock items.")
    for item in low:
        print(f'{item["name"]} | Qty: {item["quantity"]}')

MENU = ("\nInventory Management System (PS 21)\n1. Add item\n2. View items\n3. Update item"
        "\n4. Delete item\n5. Total stock value\n6. Low-stock report\n7. Search items\n8. Exit")

def main():
    try:
        while True:
            choice = input(MENU + "\nMenu option: ").strip()
            if choice == "1":
                add_item()
            elif choice == "2":
                display_items(inventory.items(), "Inventory is empty.")
            elif choice in ("3", "4"):
                change_item("update" if choice == "3" else "delete")
            elif choice == "5":
                total = sum(item["quantity"] * item["price"] for item in inventory.values())
                print(f"Total stock value: {amount(total)}")
            elif choice == "6":
                show_low_stock()
            elif choice == "7":
                search_items()
            elif choice == "8":
                break
            else:
                print("Please choose an option from 1 to 8.")
    except (EOFError, KeyboardInterrupt):
        print()
    print("Goodbye!")

if __name__ == "__main__":
    main()
