import json
import os

INVENTORY_FILE = 'inventory.json'

def load_inventory():
    """Loads inventory from the JSON file."""
    if not os.path.exists(INVENTORY_FILE):
        return []
    try:
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Error loading inventory file. Starting with an empty inventory.")
        return []

def save_inventory(inventory):
    """Saves inventory to the JSON file."""
    try:
        with open(INVENTORY_FILE, 'w') as f:
            json.dump(inventory, f, indent=4)
        print("Inventory saved successfully.")
    except IOError as e:
        print(f"Error saving inventory: {e}")

def add_product(inventory):
    """Adds a new product to the inventory."""
    print("\n--- Add New Product ---")
    name = input("Enter product name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    # Check for duplicates
    for item in inventory:
        if item['name'].lower() == name.lower():
            print("Product already exists.")
            return

    category = input("Enter category: ").strip()
    
    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))
        threshold = int(input("Enter low stock threshold: "))
    except ValueError:
        print("Invalid input. Quantity and threshold must be integers, price must be a number.")
        return

    product = {
        "name": name,
        "category": category,
        "quantity": quantity,
        "price": price,
        "low_stock_threshold": threshold,
        "sold_count": 0
    }
    inventory.append(product)
    save_inventory(inventory)
    print(f"Product '{name}' added successfully.")

def update_quantity(inventory):
    """Updates product quantity (restock or sell)."""
    print("\n--- Update Quantity ---")
    name = input("Enter product name to update: ").strip()
    
    product = None
    for item in inventory:
        if item['name'].lower() == name.lower():
            product = item
            break
            
    if not product:
        print("Product not found.")
        return

    print(f"Current quantity of '{product['name']}': {product['quantity']}")
    action = input("Type 'sell' to sell or 'restock' to add stock: ").strip().lower()
    
    if action == 'sell':
        try:
            amount = int(input("Enter quantity to sell: "))
            if amount <= 0:
                print("Quantity must be positive.")
                return
            if product['quantity'] < amount:
                print("Insufficient stock.")
                return
            product['quantity'] -= amount
            product['sold_count'] += amount
            save_inventory(inventory)
            print(f"Sold {amount} of '{product['name']}'. New quantity: {product['quantity']}")
        except ValueError:
             print("Invalid quantity.")

    elif action == 'restock':
        try:
            amount = int(input("Enter quantity to restock: "))
            if amount <= 0:
                print("Quantity must be positive.")
                return
            product['quantity'] += amount
            save_inventory(inventory)
            print(f"Restocked {amount} of '{product['name']}'. New quantity: {product['quantity']}")
        except ValueError:
             print("Invalid quantity.")
    else:
        print("Invalid action.")

def search_product(inventory):
    """Searches for products by name or category."""
    print("\n--- Search Product ---")
    query = input("Enter name or category to search: ").strip().lower()
    found = False
    for item in inventory:
        if query in item['name'].lower() or query in item['category'].lower():
            print(f"Found: {item['name']} (Category: {item['category']}, Qty: {item['quantity']}, Price: ${item['price']:.2f})")
            found = True
    if not found:
        print("No products found matching your query.")

def check_low_stock(inventory):
    """Displays products with quantity below their threshold."""
    print("\n--- Low Stock Alert ---")
    found = False
    for item in inventory:
        if item['quantity'] < item['low_stock_threshold']:
            print(f"LOW STOCK: {item['name']} (Qty: {item['quantity']}, Threshold: {item['low_stock_threshold']})")
            found = True
    if not found:
        print("No items are below their stock threshold.")

def calculate_total_value(inventory):
    """Calculates the total value of the current inventory."""
    total_value = sum(item['quantity'] * item['price'] for item in inventory)
    print(f"\nTotal Inventory Value: ${total_value:.2f}")

def show_sales_stats(inventory):
    """Shows the most and least sold items."""
    if not inventory:
        print("\nNo inventory data to analyze.")
        return
        
    sorted_items = sorted(inventory, key=lambda x: x['sold_count'], reverse=True)
    
    print("\n--- Sales Statistics ---")
    print(f"Most Sold: {sorted_items[0]['name']} ({sorted_items[0]['sold_count']} sold)")
    
    # Handle ties for least sold or just show the last one
    least_sold = sorted_items[-1]
    print(f"Least Sold: {least_sold['name']} ({least_sold['sold_count']} sold)")

def main():
    inventory = load_inventory()
    
    while True:
        print("\n=== Inventory Management System ===")
        print("1. Add New Product")
        print("2. Update Quantity (Sell/Restock)")
        print("3. Search Product")
        print("4. Show Low Stock")
        print("5. Calculate Total Inventory Value")
        print("6. Show Most/Least Sold Items")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            add_product(inventory)
        elif choice == '2':
            update_quantity(inventory)
        elif choice == '3':
            search_product(inventory)
        elif choice == '4':
            check_low_stock(inventory)
        elif choice == '5':
            calculate_total_value(inventory)
        elif choice == '6':
            show_sales_stats(inventory)
        elif choice == '7':
            save_inventory(inventory)
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
