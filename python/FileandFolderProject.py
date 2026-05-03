from pathlib import Path
import os
import shutil


def create_folder():
    try:
        name = input("Enter the name of the folder : ")
        path = Path(name)

        if not path.exists():
            path.mkdir()
            print("Folder created successfully")
        else:
            print("Folder already exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)


def read_file_folder():
    try:
        path = Path.cwd()   # current working directory
        items = list(path.iterdir())

        if not items:
            print("Directory is empty")
        else:
            for i, item in enumerate(items):
                print(f"{i + 1} : {item}")

    except Exception as err:
        print("Sorry an error occurred : ", err)


def update_folder():
    try:
        old_name = input("Enter the name of the folder you want to update : ")
        path = Path(old_name)

        if path.exists() and path.is_dir():
            new_name = input("Enter the new name of the folder : ")
            new_path = Path(new_name)

            if not new_path.exists():
                path.rename(new_path)
                print("Folder renamed successfully")
            else:
                print("A folder with that name already exists")
        else:
            print("Sorry no such folder exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)


def delete_folder():
    try:
        name = input("Enter the name of the folder you want to delete : ")
        path = Path(name)

        if path.exists() and path.is_dir():
            confirm = input("⚠️ This will delete everything inside. Type 'yes' to confirm: ")

            if confirm.lower() == "yes":
                shutil.rmtree(path)
                print("Folder deleted successfully")
            else:
                print("Deletion cancelled")
        else:
            print("Sorry no such folder exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)


def create_file():
    try:
        read_file_folder()
        name = input("Enter the name of the file you want to create : ")
        path = Path(name)

        if not path.exists():
            with open(name, 'w') as file:
                data = input("Write content : ")
                file.write(data)
            print("File created successfully")
        else:
            print("File already exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)


def read_file():
    try:
        read_file_folder()
        name = input("Enter the name of the file you want to read : ")
        path = Path(name)

        if path.exists() and path.is_file():
            with open(name, 'r') as file:
                print("\nFile Content:\n")
                print(file.read())
        else:
            print("Sorry no such file exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)


def update_file():
    try:
        read_file_folder()
        name = input("Enter the file name : ")
        path = Path(name)

        if path.exists() and path.is_file():

            while True:
                print("\nOptions:")
                print("1. Rename file")
                print("2. Append content")
                print("3. Overwrite file")
                print("4. Back")

                try:
                    choice = int(input("Enter your choice : "))
                except:
                    print("Invalid input")
                    continue

                if choice == 1:
                    new_name = input("Enter new file name : ")
                    new_path = Path(new_name)

                    if not new_path.exists():
                        path.rename(new_path)
                        print("File renamed successfully")
                        break
                    else:
                        print("File with that name already exists")

                elif choice == 2:
                    with open(name, 'a') as file:
                        data = input("Enter content to append : ")
                        file.write(data)
                    print("Content added successfully")
                    break

                elif choice == 3:
                    with open(name, 'w') as file:
                        data = input("Enter new content : ")
                        file.write(data)
                    print("File overwritten successfully")
                    break

                elif choice == 4:
                    break

                else:
                    print("Invalid choice")

        else:
            print("Sorry no such file exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)


def delete_file():
    try:
        read_file_folder()
        name = input("Enter the file name you want to delete : ")
        path = Path(name)

        if path.exists() and path.is_file():
            confirm = input("Type 'yes' to confirm deletion: ")

            if confirm.lower() == "yes":
                os.remove(name)
                print("File deleted successfully")
            else:
                print("Deletion cancelled")
        else:
            print("Sorry no such file exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)


# MAIN MENU LOOP
while True:
    print("\n===== FILE MANAGER =====")
    print("1. Create folder")
    print("2. View files/folders")
    print("3. Rename folder")
    print("4. Delete folder")
    print("5. Create file")
    print("6. Read file")
    print("7. Update file")
    print("8. Delete file")
    print("9. Exit")

    try:
        choice = int(input("Enter your choice : "))
    except:
        print("Invalid input, try again")
        continue

    if choice == 1:
        create_folder()
    elif choice == 2:
        read_file_folder()
    elif choice == 3:
        update_folder()
    elif choice == 4:
        delete_folder()
    elif choice == 5:
        create_file()
    elif choice == 6:
        read_file()
    elif choice == 7:
        update_file()
    elif choice == 8:
        delete_file()
    elif choice == 9:
        print("Exiting... 👋")
        break
    else:
        print("Invalid choice")