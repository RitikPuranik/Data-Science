from Database import conn

class Customers:
    def __init__(self):
        # self.name = name
        # self.contact = contact
        pass
    @staticmethod 
    def create_table():
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                contact VARCHAR(15) NOT NULL
            );
            """
        )
        conn.commit()
        cur.close()

    @staticmethod
    def insert_customer(name, contact):
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO customers(name, contact)
            VALUES (%s, %s)
            """, (name, contact)
        )
        conn.commit()
        cur.close()

    @staticmethod
    def update_customer(customer_id, name = None, contact = None):
            cur = conn.cursor()
            cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
            customer = cur.fetchone()

            if not customer:
                print("Customer not found.")
                cur.close()
                return

            update_fields = []
            if name:
                update_fields.append(f"name = '{name}'")
            if contact:
                update_fields.append(f"contact = '{contact}'")

            update_query = f"UPDATE customers SET {','.join(update_fields)} WHERE id = %s"

            cur.execute(update_query, (customer_id,))
            conn.commit()
            cur.close()

    @staticmethod
    def delete_customer(customer_id):
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE ID = %s", (customer_id,))
        conn.commit()
        cur.close()

    @staticmethod
    def get_all_customers():
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()
        cur.close()
        return customers
    
    @staticmethod
    def customer_menu():
        while True:
            print("\nCustomer Management Menu:")
            print("1. Create Customers Table")
            print("2. Insert Customer")
            print("3. Update Customer")
            print("4. Delete Customer")
            print("5. View All Customers")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                Customers().create_table()
                print("Customers table created successfully.")
            elif choice == '2':
                name = input("Enter customer name: ")
                contact = input("Enter customer contact: ")
                Customers().insert_customer(name, contact)
                print("Customer inserted successfully.")
            elif choice == '3':
                customer_id = int(input("Enter customer ID to update: "))
                name = input("Enter new name (leave blank to keep unchanged): ")
                contact = input("Enter new contact (leave blank to keep unchanged): ")
                Customers().update_customer(customer_id, name if name else None, contact if contact else None)
                print("Customer updated successfully.")
            elif choice == '4':
                customer_id = int(input("Enter customer ID to delete: "))
                Customers().delete_customer(customer_id)
                print("Customer deleted successfully.")
            elif choice == '5':
                customers = Customers().get_all_customers()
                for customer in customers:
                    print(f"ID: {customer[0]}, Name: {customer[1]}, Contact: {customer[2]}")
            elif choice == '6':
                print("Exiting Customer Management Menu.")
                break
            else:
                print("Invalid choice. Please try again.")









