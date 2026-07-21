# lab5_1.py

contacts = {}

while True:
    print("\n===== Contact Book =====")
    print("1. Add/Update Contact")
    print("2. View Contact Details")
    print("3. List All Contacts")
    print("4. Delete Contact")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter contact name: ").strip().lower()
        phone = input("Enter phone number: ")
        email = input("Enter email: ")

        contacts[name] = {
            "phone": phone,
            "email": email
        }

        print(f"Contact '{name}' saved successfully!")

    elif choice == "2":
        name = input("Enter contact name to view: ").strip().lower()

        contact = contacts.get(name)

        if contact:
            print(f"Name : {name.title()}")
            print(f"Phone: {contact['phone']}")
            print(f"Email: {contact['email']}")
        else:
            print("Contact not found.")

    elif choice == "3":
        if len(contacts) == 0:
            print("No contacts available.")
        else:
            print("\nAll Contacts")
            for name, details in contacts.items():
                print(f"\n{name.title()}")
                print(f" Phone : {details['phone']}")
                print(f" Email : {details['email']}")

    elif choice == "4":
        name = input("Enter contact name to delete: ").strip().lower()

        removed = contacts.pop(name, None)

        if removed:
            print("Contact deleted.")
        else:
            print("Contact not found.")

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")