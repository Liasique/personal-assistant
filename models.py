from collections import UserDict
from datetime import datetime
import re

# Базовий клас для всіх полів (має лише значення)
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
# Клас для імені контакту
class Name(Field):
    pass

# Клас для номера телефону з валідацією (10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

# Клас для дати народження з валідацією (формат YYYY-MM-DD)
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
    
# Клас для email з валідацією
class Email(Field):
    def __init__(self, value):
        # Простий regex для перевірки email
        if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", value):
            raise ValueError("Invalid email format.")
        super().__init__(value)


# Клас для адреси — без валідації, довільний текст
class Address(Field):
    pass

# Клас Note — для нотаток, які можна додавати до запису
class Note(Field):
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
    def edit_text(self, new_text):
        self.text = new_text
    def __str__(self):
        tags_str = ', '.join(self.tags) if self.tags else "No tags"
        return f"Note: {self.text}\nTags: {tags_str}"

# Record — один контакт зі всіма полями: ім'я, телефони, email, адреса, день народження
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ', '.join(str(p) for p in self.phones)
        email = str(self.email) if self.email else "No email"
        address = str(self.address) if self.address else "No address"
        birthday = str(self.birthday) if self.birthday else "No birthday"
        return (f"Name: {self.name}, Phones: {phones}, Email: {email}, "
                f"Address: {address}, Birthday: {birthday}")
    
    # AddressBook — словник контактів (ключ = ім'я)
class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Only Record instances can be added.")
        self.data[record.name.value] = record

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"No contact found with name: {name}")

    def find_record(self, name):
        return self.data.get(name, None)

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

#NoteBook — окремий клас для нотаток, які можна додавати до записів
class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.notes = [] 
    def add_note(self, note):
        if not isinstance(note, Note):
            raise TypeError ("Only Note instances can be added.")
        self.notes.append(note)

    def find_by_tag(self, tag):
        return [note for note in self.notes if tag in note.tags]
   
    def search_in_text(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.text.lower()]

    def remove_note(self, text):
        for note in self.notes:
            if note.text == text:
                self.notes.remove(note)
                return True
        return False

    def __str__(self):
        return "\n".join(str(note) for note in self.notes)
    
# Головний блок для тестування
if __name__ == "__main__":
     # Створюємо об'єкт адресної книги
    book = AddressBook()

    # Створюємо запис для контакту
    record = Record("Olga")
    record.add_phone("0671234567")
    record.add_email("olga@example.com")
    record.add_address("Kyiv, Ukraine")
    record.add_birthday("26.06.1990")

    # Додаємо запис в адресну книгу
    book.add_record(record)

    # Виводимо всі записи
    for name, rec in book.data.items():
        print(rec)

    # Додаємо нотатку до контакту
    note1 = Note("Buy milk and bread", ["shopping", "urgent"])
    print(note1)

    note1.add_tag("groceries")
    note1.remove_tag("urgent")
    note1.edit_text("Buy milk, bread, and eggs")
    print("\nAfter changes:")
    print(note1)

    print("\n--- Notebook tests ---")
    nb = NoteBook()

    note1 = Note("Buy milk and bread", tags=["shopping", "urgent"])
    note2 = Note("Read book about Python", tags=["study", "python"])
    note3 = Note("Buy flowers", tags=["shopping"])

    nb.add_note(note1)
    nb.add_note(note2)
    nb.add_note(note3)

    print("All notes:")
    print(nb)

    print("\nSearch by tag 'shopping':")
    for n in nb.find_by_tag("shopping"):
        print(n)

    print("\nSearch in text 'Python':")
    for n in nb.search_in_text("Python"):
        print(n)

    print("\nRemoving note 'Buy flowers'")
    nb.remove_note("Buy flowers")
    print(nb)