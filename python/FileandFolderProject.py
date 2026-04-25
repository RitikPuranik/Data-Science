from pathlib import Path
import os

def create_folder():
    try:
        name = input("Enter the name of the folder : ")
        path = Path(name)
        path.mkdir()
        print("Folder created successfully")
    
    except Exception as err:
        print("Sorry an erro occurred : ", err)


def read_file_folder():
    try:
        path = Path("")
        items = list(path.rglob('*'))

        #enumerate is used to get the index of the item in the list and the item itself differently
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
            new_Path = Path(new_name)
            path.rename(new_Path)
            print("Folder name updated successfully")
        else:
            print("Sorry no such folder exists")
    
    except Exception as err:
        print("Sorry an error occurred : ", err)
        

def delete_folder():
    try:
        name = input("Enter the name of the folder you want to delete : ")
        path = Path(name)

        if path.exists() and path.is_dir():
            path.rmdir()
            print("Folder deleted successfully")
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
                data = input("Write what you want to write in the file :    ")
                file.write(data)
            print("File created successfully")
        else:
            print("Sorry a file with the same name already exists")
    
    except Exception as err:
        print("Sorry an error occurred : ", err)



def read_file():
    try:
        read_file_folder()
        name = input("Enter the name of the file you want to read : ")
        path = Path(name)

        if path.exists() and path.is_file():
            with open(name, 'r') as file:
                content = file.read()
                print("Your file content is :   ")
                print(content)
        else:
            print("Sorry no such file exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)


def update_file():
    try:
        read_file_folder()
        name = input("Enter the name of the file you want to update : ")
        path = Path(name)

        if path.exists() and path.is_file():

            print("Options : ")
            print("1. Renaming the file")
            print("2. Adding more content to the file")
            print("3. Overwriting the file")

            choice = int(input("Enter your choice : "))

            if choice == 1:
                new_name = input("Enter the new name of the file : ")
                new_path = Path(new_name)

                if not new_path.exists():
                    path.rename(new_path)
                    print("File renamed successfully")
                else:
                    print("Sorry a file with the same name already exists")

            elif choice == 2:
                with open(name, 'a') as file:
                    data = input("Write what you want to add in the file :    ")
                    file.write(data)
                print("File updated successfully")

            elif choice == 3:
                with open(name, 'w') as file:
                    data = input("Write what you want to write in the file :    ")
                    file.write(data)
                print("File updated successfully")
            
            else:
                print("Invalid choice")
                update_file()

        else:
            print("Sorry no such file exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)


def delete_file():
    try:
        read_file_folder()
        name = input("Enter the name of the file you want to delete : ")
        path = Path(name)

        if path.exists() and path.is_file():
            os.remove(name)
            print("File deleted successfully")
        else:
            print("Sorry no such file exists")

    except Exception as err:
        print("Sorry an error occurred : ", err)




print("Options :")

print("1. Create a folder")
print("2. Read files and folders")
print("3. Update the folder")
print("4. Delete the folder")
print("5. Creation of a file")
print("6. Read the file")
print("7. Update a file")
print("8. Delete a file")

choice = int(input("Enter your choice : "))

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

else:
    print("Invalid choice")
