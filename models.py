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