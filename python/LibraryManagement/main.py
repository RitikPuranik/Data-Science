import json
import random
import string
from pathlib import Path
from datetime import datetime


class Library:
    BASE_DIR = Path(__file__).resolve().parent
    database = BASE_DIR / "library.json"
    data = {"books" : [], "members" : []}

    #load existing data to JSON 
    if Path(database).exists():
        with open(database, "r") as file:
            content = file.read().strip()

            if content:
                data = json.loads(content)
    
    else:
        with open(database, "w") as file:
            json.dump(data, file, indent=4)



    #made so noboady from outside can use this 
    @classmethod
    def save_data(cls):
        with open(cls.database, "w") as file:
            json.dump(cls.data, file, indent=4, default=str)



    @staticmethod
    def generate_id(Prefix = "B"):
        random_id = ""
        for i in range(5):
            random_id += random.choice(string.ascii_uppercase + string.digits)

        return Prefix + "-" + random_id



    def add_book(self):
        try:
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            copies = int(input("Enter number of copies: "))

            if copies <= 0:
                print("❌ Copies must be greater than 0.")
                return

            book = {
                "id": Library.generate_id(),
                "title": title,
                "author": author,
                "total_copies": copies,
                "available_copies": copies,
                "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            Library.data['books'].append(book)
            Library.save_data()

            print(f"✅ Book '{title}' added successfully with ID {book['id']}.")

        except ValueError:
            print("❌ Please enter a valid number for copies.")
    


    def list_books(self):
        books = Library.data.get('books', [])

        if not books:
            print("📭 No books available.")
            return

        print(f"{'No.':<5} {'ID':<10} {'Title':<20} {'Author':<15} {'Avail':<10}")
        print("-" * 70)

        for i, book in enumerate(books, start=1):
            print(f"{i:<5} {book.get('id',''):<10} {book.get('title',''):<20} {book.get('author',''):<15} {book.get('available_copies',0)}/{book.get('total_copies',0):<10}")



    def add_member(self):
        name = input("Enter member name: ").strip()
        email = input("Enter member email: ").strip()

        if not name or not email:
            print("❌ Name and email cannot be empty.")
            return

        member = {
            "id": Library.generate_id("M"),
            "name": name,
            "email": email,
            "borrowed": [],
            "joined_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        Library.data['members'].append(member)
        Library.save_data()

        print(f"✅ Member {name} added with ID {member['id']}.")



    def list_members(self):
        members = Library.data.get('members', [])

        if not members:
            print("📭 No members found.")
            return

        print(f"{'ID':<10} {'Name':<20} {'Email':<30} {'Borrowed':<20}")
        print("-" * 90)

        for m in members:
            borrowed_titles = ", ".join([b['title'] for b in m['borrowed']]) if m['borrowed'] else "None"
            print(f"{m['id']:<10} {m['name']:<20} {m['email']:<30} {borrowed_titles:<20}")



    def borrow_book(self):
        member_id = input("Enter member ID: ").strip()

        members = [m for m in Library.data['members'] if m['id'] == member_id]
        if not members:
            print("❌ Member not found.")
            return

        member = members[0]

        books = Library.data['books']
        if not books:
            print("📭 No books available.")
            return

        print("\n📚 Available Books:")
        print("-" * 50)

        available_books = [b for b in books if b['available_copies'] > 0]

        if not available_books:
            print("❌ No books currently available.")
            return

        for i, b in enumerate(available_books, start=1):
            print(f"{i}. {b['title']} (Available: {b['available_copies']})")

        try:
            choice = int(input("Enter number of book to borrow: "))

            if choice < 1 or choice > len(available_books):
                print("❌ Invalid choice.")
                return

            book = available_books[choice - 1]

            if any(b['book_id'] == book['id'] for b in member['borrowed']):
                print("⚠️ You already borrowed this book.")
                return

            borrow_entry = {
                "book_id": book['id'],
                "title": book['title'],
                "borrowed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            member['borrowed'].append(borrow_entry)
            book['available_copies'] -= 1

            Library.save_data()

            print(f"✅ Borrowed '{book['title']}' successfully!")

        except ValueError:
            print("❌ Enter a valid number.")
            member_id = input("Enter member ID: ").strip()
            members = [m for m in Library.data['members'] if m['id'] == member_id]
            if not members:
                print("Member not found.")
                return 
            member = members[0]

            book_id = input("Enter book ID to borrow: ").strip()
            books = [b for b in Library.data['books'] if b['id'] == book_id]
            if not books:
                print("Book not found.")
                return
            book = books[0]


            if book['available_copies'] <= 0:
                print("Sorry, this book is currently unavailable.")
                return
            if book_id in member['borrowed']:
                print("You have already borrowed this book.")
                return
            
            borrow_entry = {
                "book_id": book_id,
                "title": book['title'],
                "borrowed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            member['borrowed'].append(borrow_entry)
            book['available_copies'] -= 1
            Library.save_data()
            print(f"You have successfully borrowed '{book['title']}'.")



    def return_book(self):
        member_id = input("Enter member ID: ").strip()

        try:
            members = [m for m in Library.data['members'] if m['id'] == member_id]
            if not members:
                print("❌ Member not found.")
                return

            member = members[0]

            if not member['borrowed']:
                print("📭 You have not borrowed any books.")
                return

            print("\n📚 Your Borrowed Books:")
            print("-" * 40)

            for i, b in enumerate(member['borrowed'], start=1):
                print(f"{i}. {b['title']} (ID: {b['book_id']}, Borrowed on: {b['borrowed_on']})")

            print("-" * 40)

            choice = int(input("Enter number of book to return: "))

            if choice < 1 or choice > len(member['borrowed']):
                print("❌ Invalid choice.")
                return

            book = member['borrowed'][choice - 1]
            book_id = book['book_id']

            # Remove from member
            member['borrowed'].remove(book)

            # Update library stock
            for b in Library.data['books']:
                if b['id'] == book_id:
                    b['available_copies'] += 1
                    break

            Library.save_data()

            print(f"✅ Book '{book['title']}' returned successfully!")

        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")



library = Library()
while True:
    print("=" * 50)
    print("Welcome to the Library Management System")
    print("=" * 50)
    print("1. Add a new book")
    print("2. View all books")
    print("3. Add a new member")
    print("4. View all members")
    print("5. Borrow a book")
    print("6. Return a book")
    print("7. Exit")
    print("-" * 50)
    choice = input("Enter your choice: ")


    if choice == "1":
        library.add_book()

    elif choice == "2":
        library.list_books()

    elif choice == "3":
        library.add_member()

    elif choice == "4":
        library.list_members()

    elif choice == "5":
        library.borrow_book()

    elif choice == "6":
        library.return_book()

    elif choice == "7":
        print("Thank you for using the Library Management System. Goodbye!")
        exit()