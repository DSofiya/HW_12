from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value) -> None:
        self.value = value


class Name(Field):
    def __init__(self, value):
        self.value = value
    

class Phone(Field):
    def __init__(self, value):
        self.value = value
    
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if value is not None and not self.is_valid_phone(value):
            raise ValueError("Invalid input. Phone number should contain only digits.")
        self.value = value

    def is_valid_phone(self, phone):
        return all(char.isdigit() for char in phone)

class Birthday(Field):
    def __init__(self, value=None):
        if isinstance(value, str):
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Incorrect date format. Device format: 1997-05-03")
        self.value = value

    def is_valid_date(self, date):
        return isinstance(date, str)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if value is not None and not self.is_valid_date(value):
            raise ValueError("Incorrect date format. Device format: 1997-05-03")
        instance.__dict__[self.name] = value

class Record:
    def __init__(self, name: str, phones: list, birthday=None):
        self.name = name
        self.phones = [phones]
        self.birthday = Birthday(birthday) if birthday is not None else None

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)
    
    def remove_phone(self, phone):
        phone_obj = Phone(phone)
        if phone_obj in self.phones:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday_year = today.year
            if today > datetime(today.year, self.birthday.value.month, self.birthday.value.day):
                next_birthday_year += 1

            next_birthday = datetime(next_birthday_year, self.birthday.value.month, self.birthday.value.day)
            days_remaining = (next_birthday - today).days
            return days_remaining
        return None 


class AddressBook():
    def __iter__(self):
        return self.iterator()
      
    def __init__(self):
        self.contacts = {}

    # def iterator(self, page_size=10):
    #     items = list(self.data.items())
    #     num_pages = (len(items) + page_size - 1) // page_size
    #     for page in range(num_pages):
    #         start = page * page_size
    #         end = start + page_size
    #         yield items[start:end]

    
    def add_contact(self, name, phone):
        self.contacts[name] = phone

    def find_contact(self, query):
        results = {}
        for name, phone in self.contacts.items():
            if query in name or query in phone:
                results[name] = phone
        return results

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.contacts = pickle.load(file)
        except FileNotFoundError:
            self.contacts = {}


contact_list = AddressBook()

def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "ValueError. Please enter the name and phone number."
        except IndexError:
            return "IndexError. Give me name and phone please."
        except NameError:
            return "Invalid input. Name should contain only letters."
        except TypeError:
            return "Invalid input. Phone number should contain only digits."
    return wrapper


@input_error
def command_add(input_str):
    name, phone = input_str.split()
    name = name.title()
    if not phone.isdigit():
        raise TypeError
    if not name.isalpha():
        raise NameError 
    contact_list.add_contact(name, phone)
    return f"Contact {name} with phone number {phone} has been added."

# @input_error
# def command_phone(input_str):
#     list_comand = input_str.split()
#     name = list_comand[1].title()
#     if not name.isalpha():
#         raise NameError
#     return contact_list[name]

@input_error
def command_change(input_str):
    name, phone = input_str.split()
    name = name.title()
    if not phone.isdigit():
        raise TypeError
    if not name.isalpha():
        raise NameError 
    contact_list.add_contact(name, phone)
    return f"Phone number for {name} has been updated to {phone}."


def command_show_all(contact_list):
    if not contact_list.contacts:
        return "Список контактів пустий."
    result = "Contacts:\n"
    for name, phone in contact_list.contacts.items():
        result += f"{name}: {phone}\n"
    return result.strip()

   
def main():  
    while True:
      

        input_str = input("Enter command: ").lower().strip()
        
        if input_str == "hello":
            filename = "AddressBook"
            contact_list.load_from_file(filename)
            print("How can I help you?")
        elif input_str.startswith("add"):
            input_str = input("Введіть ім'я контакту та номер телефону: ")
            print(command_add(input_str))  
        elif input_str.startswith("change"):
            input_str = input("Введіть ім'я контакту та номер телефону: ")
            print(command_add(input_str))
        elif input_str.startswith("phone"):
            print(command_phone(input_str))
        elif input_str == "show all":
            print(command_show_all(contact_list))
        elif input_str == "find":
            query = input("Введіть ім'я або номер телефону для пошуку: ")
            results = contact_list.find_contact(query)
            if results:
                print("Результати пошуку:")
                for name, phone in results.items():
                    print(f"Ім'я: {name}, Номер телефону: {phone}")
            else:
                print("Нічого не знайдено.")
        elif input_str == "save":
            filename = "AddressBook"
            contact_list.save_to_file(filename)
            print(f"Адресну книгу збережено у файлі {filename}.")
        elif input_str == "load":
            filename = "AddressBook"
            contact_list.load_from_file(filename)
            print(f"Адресну книгу завантажено з файлу {filename}.")    
        elif input_str in ["good bye", "close", "exit"]:
            filename = "AddressBook"
            contact_list.save_to_file(filename)
            print("Good bye!")
            break
        else:
            print("Невірно введена команда. Доступні команди:")
            print("Привітатись - 'hello'")
            print("Додати контакт -'add'")
            print("Змінити контакт -'change'")
            print("Додати телефон -'phone'")
            print("Переглянути всі контакти -'show all'")
            print("Знайти контакт -'find'")
            print("Зберегти адресну книгу - 'save'")
            print("Завантажити адресну книгу - 'load'")
            print("Вийти - 'good bye','close','exit'")



if __name__ == "__main__":
    main()
