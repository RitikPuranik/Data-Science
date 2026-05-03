import streamlit as st
import json
import random
import string
from pathlib import Path
from datetime import datetime

# ----------------- Backend Logic (Same as yours, slightly adapted) -----------------

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "library.json"

if DATABASE.exists():
    with open(DATABASE, "r") as f:
        content = f.read().strip()
        data = json.loads(content) if content else {"books": [], "members": []}
else:
    data = {"books": [], "members": []}
    with open(DATABASE, "w") as f:
        json.dump(data, f)

def save_data():
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4, default=str)

def generate_id(prefix="B"):
    return prefix + "-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))


# ----------------- UI -----------------

st.set_page_config(page_title="📚 Library System", layout="wide")

st.title("📚 Library Management System")

menu = st.sidebar.selectbox("Choose Action", [
    "Add Book",
    "View Books",
    "Add Member",
    "View Members",
    "Borrow Book",
    "Return Book"
])

# ----------------- Add Book -----------------
if menu == "Add Book":
    st.header("➕ Add Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    copies = st.number_input("Number of Copies", min_value=1, step=1)

    if st.button("Add Book"):
        book = {
            "id": generate_id(),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data["books"].append(book)
        save_data()
        st.success(f"Book '{title}' added!")

# ----------------- View Books -----------------
elif menu == "View Books":
    st.header("📖 All Books")

    if not data["books"]:
        st.info("No books available")
    else:
        st.table(data["books"])

# ----------------- Add Member -----------------
elif menu == "Add Member":
    st.header("👤 Add Member")

    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Add Member"):
        member = {
            "id": generate_id("M"),
            "name": name,
            "email": email,
            "borrowed": [],
            "joined_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data["members"].append(member)
        save_data()
        st.success(f"Member '{name}' added!")

# ----------------- View Members -----------------
elif menu == "View Members":
    st.header("👥 Members")

    if not data["members"]:
        st.info("No members found")
    else:
        st.table(data["members"])

# ----------------- Borrow Book -----------------
elif menu == "Borrow Book":
    st.header("📥 Borrow Book")

    member_ids = [m["id"] for m in data["members"]]
    member_id = st.selectbox("Select Member", member_ids)

    available_books = [b for b in data["books"] if b["available_copies"] > 0]

    if not available_books:
        st.warning("No books available")
    else:
        book_titles = [b["title"] for b in available_books]
        selected_book = st.selectbox("Select Book", book_titles)

        if st.button("Borrow"):
            member = next(m for m in data["members"] if m["id"] == member_id)
            book = next(b for b in available_books if b["title"] == selected_book)

            borrow_entry = {
                "book_id": book["id"],
                "title": book["title"],
                "borrowed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            member["borrowed"].append(borrow_entry)
            book["available_copies"] -= 1

            save_data()
            st.success(f"Borrowed '{book['title']}'")

# ----------------- Return Book -----------------
elif menu == "Return Book":
    st.header("📤 Return Book")

    member_ids = [m["id"] for m in data["members"]]
    member_id = st.selectbox("Select Member", member_ids)

    member = next(m for m in data["members"] if m["id"] == member_id)

    if not member["borrowed"]:
        st.info("No borrowed books")
    else:
        borrowed_titles = [b["title"] for b in member["borrowed"]]
        selected_book = st.selectbox("Select Book to Return", borrowed_titles)

        if st.button("Return"):
            book_entry = next(b for b in member["borrowed"] if b["title"] == selected_book)
            member["borrowed"].remove(book_entry)

            for b in data["books"]:
                if b["id"] == book_entry["book_id"]:
                    b["available_copies"] += 1

            save_data()
            st.success(f"Returned '{selected_book}'")