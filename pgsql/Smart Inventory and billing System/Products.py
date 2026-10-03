from Database import conn

class Products:

    def __init__(self):
        pass

    @staticmethod 
    def create_table():
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                quantity INTEGER NOT NULL
            );
            """
        )
        conn.commit()
        cur.close()

    @staticmethod
    def insert_product(name, description, price, quantity):
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO products(name, description, price, quantity)
            VALUES (%s, %s, %s, %s)
            """, (name, description, price, quantity)
        )
        conn.commit()
        cur.close()

    @staticmethod
    def update_product(product_id, name = None, description = None, price = None, quantity = None):
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cur.fetchone()

            if not product:
                print("Product not found.")
                cur.close()
                return

            update_fields = []
            if name:
                update_fields.append(f"name = '{name}'")
            if description:
                update_fields.append(f"description = '{description}'")
            if price:
                update_fields.append(f"price = {price}")
            if quantity:
                update_fields.append(f"quantity = {quantity}")

            update_query = f"UPDATE products SET {','.join(update_fields)} WHERE id = %s"

            cur.execute(update_query, (product_id,))
            conn.commit()
            cur.close()

    @staticmethod
    def delete_product(product_id):
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE ID = %s", (product_id,))
        conn.commit()
        cur.close()

    @staticmethod
    def get_all_products():
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        cur.close()
        return products
    
    @staticmethod
    def product_menu():
        while True:
            print("\n Products Management Menu:")
            print("1. Create Products Table")
            print("2. Insert Product")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. View All Products")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                Products().create_table()
                print("Products table created successfully.")
            elif choice == '2':
                name = input("Enter product name: ")
                description = input("Enter product description: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                Products().insert_product(name, description, price, quantity)
                print("Product inserted successfully.")
            elif choice == '3':
                products_id = int(input("Enter product ID to update: "))
                name = input("Enter new name (leave blank to keep unchanged): ")
                description = input("Enter new description (leave blank to keep unchanged): ")
                price = input("Enter new price (leave blank to keep unchanged): ")
                quantity = input("Enter new quantity (leave blank to keep unchanged): ")
                Products().update_product(products_id, name if name else None, description if description else None, float(price) if price else None, int(quantity) if quantity else None)
                print("Product updated successfully.")
            elif choice == '4':
                product_id = int(input("Enter product ID to delete: "))
                Products().delete_product(product_id)
                print("Product deleted successfully.")
            elif choice == '5':
                products = Products().get_all_products()
                for product in products:
                    print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Quantity: {product[4]}")
            elif choice == '6':
                print("Exiting Product Management Menu.")
                break
            else:
                print("Invalid choice. Please try again.")


