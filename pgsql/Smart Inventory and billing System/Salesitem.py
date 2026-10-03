from Database import conn

class SaleItems:
    def __init__(self):
        pass

    @staticmethod
    def create_table():
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sales_items (
                id SERIAL PRIMARY KEY,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10, 2) NOT NULL
            );
            """
        )
        conn.commit()
        cur.close()

    @staticmethod
    def insert_sale_item(sale_id, product_id, quantity, price):
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO sales_items(sale_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
            """, (sale_id, product_id, quantity, price)
        )
        conn.commit()
        cur.close()
    