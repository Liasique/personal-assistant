from models import AddressBook, NoteBook, Record, Note
import sys
# added first contact for testing
#
""" 
book = AddressBook()
record = Record("Olga")
record.add_phone("0671234567")
record.add_email("olga@example.com")
record.add_address("Kyiv, Ukraine")
record.add_birthday("26.06.1990")
book.add_record(record)
book.save_to_file()
"""
def main():
    # Завантажуємо адресну книгу з файлу або створюємо нову
    book = AddressBook()
    book.load_from_file()

    # Завантажуємо нотатки
    notebook = NoteBook()
    notebook.load_from_file()

    print("📒 Personal Assistant started. Type 'help' to see available commands.")

    while True:
        command = input("\nEnter a command: ").strip().lower()
        if command == "exit":
            print("💾 Saving data...")
            book.save_to_file()
            notebook.save_to_file()
            print("👋 Goodbye!")
            break

        elif command == "help":
           print("""
Available commands:
  add          - Add a new contact
  show all     - Show all contacts
  find         - Find a contact by name
  delete       - Delete a contact by name
  notes        - Show all notes
  help         - Show this help message
  exit         - Save and exit
""")
        elif command == "add":
            name = input("Enter name: ").strip()
            record = Record(name)

            phone = input("Enter phone (optional): ").strip()
            if phone:
                record.add_phone(phone)

            email = input("Enter email (optional): ").strip()
            if email:
                record.add_email(email)

            address = input("Enter address (optional): ").strip()
            if address:
                record.add_address(address)

            birthday = input("Enter birthday (optional, format DD.MM.YYYY): ").strip()
            if birthday:
                try:
                    record.add_birthday(birthday)
                except ValueError as e:
                    print(f"⚠️ {e}")
        # else:
        #     print("⚠️ Unknown command. Type 'help' to see available commands.")

            book.add_record(record)
            print("✅ Contact added successfully.")

        elif command == "show all":
            if not book.data:
                print("📭 Address book is empty.")
            else:
                for record in book.data.values():
                    print(record)

        elif command == "find":
            name = input("Enter the name to search: ").strip()
            found = None
            for contact_name, record in book.data.items():
                if contact_name.lower() == name.lower():
                    found = record
                    break
            if found:
                print(found)
            else:
                print(f"❌ No contact found with name '{name}'")

        elif command == "delete":
            name = input("Enter the name to delete: ").strip()
            deleted = False
            for contact_name in list(book.data.keys()):
                if contact_name.lower() == name.lower():
                    book.remove_record(contact_name)
                    print(f"🗑️ Contact '{contact_name}' deleted successfully.")
                    deleted = True
                    break
            if not deleted:
                print(f"❌ No contact found with name '{name}'")

        elif command == "edit":
            name = input("Enter the name of the contact to edit: ").strip()
            record = book.find_record(name)
            if record:
                print(f"Editing contact: {record}")
                phone = input("Enter new phone (leave empty to keep current): ").strip()
                if phone:
                    record.edit_phone(record.phones[0].value, phone)

                email = input("Enter new email (leave empty to keep current): ").strip()
                if email:
                    record.add_email(email)

                address = input("Enter new address (leave empty to keep current): ").strip()
                if address:
                    record.add_address(address)

                birthday = input("Enter new birthday (leave empty to keep current): ").strip()
                if birthday:
                    try:
                        record.add_birthday(birthday)
                    except ValueError as e:
                        print(f"⚠️ {e}")

                print("✅ Contact updated successfully.")
            else:
                print(f"❌ No contact found with name '{name}'")




if __name__ == "__main__":
    main()
