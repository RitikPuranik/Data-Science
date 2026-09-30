from Database import conn

class Sales:
    
    def __init__(self):
        pass

    @staticmethod 
    def sales_table():
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                date DATE NOT NULL, 
                total_amount DECIMAL(10, 2) NOT NULL,
            );
            """
        )
        conn.commit()
        cur.close()

    @staticmethod
    def insert_sale(customer_id, date, total_amount):
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO sales(customer_id, date, total_amount)
            VALUES (%s, %s, %s)
            """, (customer_id, date, total_amount)
        )
        conn.commit()
        cur.close()

    @staticmethod
    def update_sale(sale_id,  customer_id = None, date = None, total_amount = None):
            cur = conn.cursor()
            cur.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
            sale = cur.fetchone()

            if not sale:
                print("Sale not found.")
                cur.close()
                return

            update_fields = []
            if customer_id:
                update_fields.append(f"customer_id = {customer_id}")
            if date:
                update_fields.append(f"date = '{date}'")
            if total_amount:
                update_fields.append(f"total_amount = {total_amount}")

            update_query = f"UPDATE sales SET {','.join(update_fields)} WHERE id = %s"

            cur.execute(update_query, (sale_id,))
            conn.commit()
            cur.close()

    @staticmethod
    def delete_sale(sale_id):
        cur = conn.cursor()
        cur.execute("DELETE FROM sales WHERE ID = %s", (sale_id,))
        conn.commit()
        cur.close()

    @staticmethod
    def get_all_sales():
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales")
        sales = cur.fetchall()
        cur.close()
        return sales

    @staticmethod
    def generate_bill(sale_id):
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
        sale_items = cur.fetchall()
        total_amount = sum(item[3] * item[4] for item in sale_items)

        for item in sale_items:
            print(f"Sale ID: {item[0]}, Customer ID: {item[1]}, Date: {item[2]}, Total Amount: {item[3]}, Quantity: {item[4]}")

        cur.close()
        return total_amount

    @staticmethod
    def  total_sales_by_date(start_date, end_date):
        cur = conn.cursor()
        cur.execute(
            """
            SELECT SUM(total_amount) FROM sales WHERE date BETWEEN %s AND %s
            """, (start_date, end_date)
        )
        total_sales = cur.fetchone()[0]
        cur.close()
        return total_sales

    @staticmethod
    def total_sales_by_customer(customer_id):
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM sales WHERE customer_id = %s
            """, (customer_id,)
        )
        sales = cur.fetchall()
        cur.close()
        return sales
    
    @staticmethod
    def  get_top_selling_products(start_date, end_date):
        cur = conn.cursor()
        cur.execute(
            """
            SELECT product_id, SUM(quantity) as total_sold FROM sales WHERE date BETWEEN %s AND %s 
            GROUP BY product_id ORDER BY total_sold DESC 
            LIMIT 5
            """, (start_date, end_date)
        )
        total_sales = cur.fetchall()[0]
        cur.close()
        return total_sales
    
    @staticmethod
    def sale_menu():
        while True:
            print("\n Sales Management Menu:")
            print("1. Create Sales Table")
            print("2. Insert Sale")
            print("3. Update Sale")
            print("4. Delete Sale")
            print("5. View All Sales")
            print("6. Generate Bill")
            print("7. Total Sales by Date")
            print("8. Total Sales by Customer")
            print("9. Top Selling Products")
            print("10. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                Sales().sales_table()
                print("Sales table created successfully.")
            elif choice == '2':
                customer_id = int(input("Enter customer ID: "))
                date = input("Enter sale date: ")
                total_amount = float(input("Enter total amount: "))
                Sales().insert_sale(customer_id, date, total_amount)
                print("Sale inserted successfully.")
            elif choice == '3':
                sale_id = int(input("Enter sale ID to update: "))
                customer_id = input("Enter new customer ID (leave blank to keep unchanged): ")
                date = input("Enter new date (leave blank to keep unchanged): ")
                total_amount = input("Enter new total amount (leave blank to keep unchanged): ")
                Sales().update_sale(sale_id, customer_id if customer_id else None, date if date else None, float(total_amount) if total_amount else None)
                print("Sale updated successfully.")
            elif choice == '4':
                sale_id = int(input("Enter sale ID to delete: "))
                Sales().delete_sale(sale_id)
                print("Sale deleted successfully.")
            elif choice == '5':
                sales = Sales().get_all_sales()
                for sale in sales:
                    print(f"ID: {sale[0]}, Customer ID: {sale[1]}, Date: {sale[2]}, Total Amount: {sale[3]}")
            elif choice == '6':
                sale_id = int(input("Enter sale ID to generate bill: "))
                total_amount = Sales().generate_bill(sale_id)
                print(f"Total Amount: {total_amount}")
            elif choice == '7':
                start_date = input("Enter start date: ")
                end_date = input("Enter end date: ")
                total_sales = Sales().total_sales_by_date(start_date, end_date)
                print(f"Total Sales: {total_sales}")
            elif choice == '8':
                customer_id = int(input("Enter customer ID: "))
                total_sales = Sales().total_sales_by_customer(customer_id)
                print(f"Total Sales: {total_sales}")
            elif choice == '9':
                start_date = input("Enter start date: ")
                end_date = input("Enter end date: ")
                top_products = Sales().get_top_selling_products(start_date, end_date)
                for product in top_products:
                    print(f"Product ID: {product[0]}, Total Sold: {product[1]}")
            elif choice == '10':
                print("Exiting Sales Management Menu.")
                break
            else:
                print("Invalid choice. Please try again.")

