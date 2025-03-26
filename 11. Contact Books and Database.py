import sqlite3

def create_table():
    """Creates the contacts table if it doesn't exist."""
    conn = sqlite3.connect("contacts experiment.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            name TEXT PRIMARY KEY,
            phone TEXT,
            email TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_contact(contacts):
    """Adds a new contact to the database."""
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")
    address = input("Enter address: ")

    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                       (name, phone, email, address))
        conn.commit()
        print(f"{name} added to contacts.")
    except sqlite3.IntegrityError:
        print(f"Contact with name '{name}' already exists.")
    conn.close()

def view_contacts(contacts):
    """Displays a list of all contacts from the database."""
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM contacts")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("Contact book is empty.")
    else:
        print("\n--- Contact List ---")
        for row in rows:
            print(f"Name: {row[0]}, Phone: {row[1]}")

def search_contact(contacts):
    """Searches for contacts by name or phone number in the database."""
    search_term = input("Enter name or phone number to search: ")
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email, address FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                   ('%' + search_term + '%', '%' + search_term + '%'))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("Contact not found.")
    else:
        for row in rows:
            print(f"\nName: {row[0]}")
            print(f"Phone: {row[1]}")
            print(f"Email: {row[2]}")
            print(f"Address: {row[3]}")

def update_contact(contacts):
    """Updates contact details in the database."""
    name_to_update = input("Enter the name of the contact to update: ")
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT phone, email, address FROM contacts WHERE name = ?", (name_to_update,))
    row = cursor.fetchone()

    if row:
        print(f"Current details for {name_to_update}:")
        print(f"Phone: {row[0]}")
        print(f"Email: {row[1]}")
        print(f"Address: {row[2]}")

        new_phone = input("Enter new phone number (or press Enter to keep current): ")
        new_email = input("Enter new email (or press Enter to keep current): ")
        new_address = input("Enter new address (or press Enter to keep current): ")

        if new_phone:
            cursor.execute("UPDATE contacts SET phone = ? WHERE name = ?", (new_phone, name_to_update))
        if new_email:
            cursor.execute("UPDATE contacts SET email = ? WHERE name = ?", (new_email, name_to_update))
        if new_address:
            cursor.execute("UPDATE contacts SET address = ? WHERE name = ?", (new_address, name_to_update))
        conn.commit()
        print(f"{name_to_update} details updated.")
    else:
        print("Contact not found.")
    conn.close()

def delete_contact(contacts):
    """Deletes a contact from the database."""
    name_to_delete = input("Enter the name of the contact to delete: ")
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = ?", (name_to_delete,))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"{name_to_delete} deleted from contacts.")
    else:
        print("Contact not found.")
    conn.close()

def main():
    """Main function to run the contact book application with database."""
    create_table()  # Create the table if it doesn't exist

    while True:
        print("\n--- Contact Book ---")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_contact({})  # contacts dictionary is not used anymore
        elif choice == "2":
            view_contacts({})
        elif choice == "3":
            search_contact({})
        elif choice == "4":
            update_contact({})
        elif choice == "5":
            delete_contact({})
        elif choice == "6":
            print("Exiting Contact Book.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()