import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('store.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

conn.commit()

# Function to add a new product
def add_product(name, price, quantity):
    cursor.execute('''
    INSERT INTO products (name, price, quantity)
    VALUES (?, ?, ?)
    ''', (name, price, quantity))
    conn.commit()
    print(f"Product '{name}' added successfully!")

# Function to update a product
def update_product(product_id, name=None, price=None, quantity=None):
    if name:
        cursor.execute('''
        UPDATE products
        SET name = ?
        WHERE id = ?
        ''', (name, product_id))
    if price:
        cursor.execute('''
        UPDATE products
        SET price = ?
        WHERE id = ?
        ''', (price, product_id))
    if quantity:
        cursor.execute('''
        UPDATE products
        SET quantity = ?
        WHERE id = ?
        ''', (quantity, product_id))
    conn.commit()
    print(f"Product ID {product_id} updated successfully!")

# Function to display all products
def display_products():
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Price: ₹{product[2]:.2f}, Quantity: {product[3]}")

# Function to make a purchase
def make_purchase(product_id, quantity):
    cursor.execute('SELECT price, quantity FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    if product:
        price, available_quantity = product
        if available_quantity >= quantity:
            total_price = price * quantity
            cursor.execute('''
            INSERT INTO purchases (product_id, quantity, total_price)
            VALUES (?, ?, ?)
            ''', (product_id, quantity, total_price))
            cursor.execute('''
            UPDATE products
            SET quantity = quantity - ?
            WHERE id = ?
            ''', (quantity, product_id))
            conn.commit()
            print(f"Purchase successful! Total price: ${total_price:.2f}")
        else:
            print("Insufficient quantity available!")
    else:
        print("Product not found!")

# Function to display all purchases
def display_purchases():
    cursor.execute('''
    SELECT purchases.id, products.name, purchases.quantity, purchases.total_price
    FROM purchases
    JOIN products ON purchases.product_id = products.id
    ''')
    purchases = cursor.fetchall()
    for purchase in purchases:
        print(f"Purchase ID: {purchase[0]}, Product: {purchase[1]}, Quantity: {purchase[2]}, Total Price: ${purchase[3]:.2f}")

# Main menu
def main():
    while True:
        print("\nStore Management System")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Display Products")
        print("4. Make Purchase")
        print("5. Display Purchases")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            add_product(name, price, quantity)
        elif choice == '2':
            product_id = int(input("Enter product ID to update: "))
            name = input("Enter new name (leave blank to skip): ")
            price = input("Enter new price (leave blank to skip): ")
            quantity = input("Enter new quantity (leave blank to skip): ")
            update_product(product_id, name or None, float(price) if price else None, int(quantity) if quantity else None)
        elif choice == '3':
            display_products()
        elif choice == '4':
            product_id = int(input("Enter product ID to purchase: "))
            quantity = int(input("Enter quantity to purchase: "))
            make_purchase(product_id, quantity)
        elif choice == '5':
            display_purchases()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

conn.close()