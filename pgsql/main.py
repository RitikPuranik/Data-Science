

from Customers import Customers
from Products import Products
from Sales import Sales

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Customer Management")
        print("2. Product Management")
        print("3. Sales Management")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            Customers().customer_menu()
        elif choice == '2':
            Products().product_menu()
        elif choice == '3':
            Sales().sale_menu()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")  

main_menu()