'''Винесені в окремий файл функції нашого бота для кращої організації та читабельності'''

import pickle
from pathlib import Path # Використовуємо для коретного отримання шляху
from adressbook import Record
from adressbook import AddressBook


# Внутрішні функці для оптимізації роботи
def input_error(func):
    '''Декоратор який обробляє помилки ValueError, KeyError, IndexError'''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return str(e)
        except KeyError:
            return 'User doesn\'t exist'
        except FileNotFoundError as e:
            print('Adressbook will be created when program done!')
            return AddressBook() # Повернення нової адресної книги, якщо файл не знайдено
    return inner

def parse_input(user_input):
    '''Ця функція обробляє введене користувачем значення'''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Функції для збереження даних
def save_data(book, filename="addressbook.pkl"):
    '''Функція насправді перезаписує файл повністю, щоразу при закритті
    програми, в майбутньому можна оптимізувати більш коректне додавання
    чи видалення записів, щоб  не перезаписувати'''
    with open(Path(f'./{filename}'), "wb") as f:
        pickle.dump(book, f)

@input_error
def load_data(filename="addressbook.pkl"):
    '''Функція додаткового обгорнута декоратором щоб сповіщати користувача
    що файл не був створений раніше, і функція його створить у разі якщо
    файл з записами був відсутній'''
    with open(Path(f'./{filename}'), "rb") as f:
        return pickle.load(f)


# Функції для роботи з запитами користувача
@ input_error
def add_contact(args, book):
    '''Ця функція додає користувача в книгу'''
    name, phone, *_ = args
    name = name.capitalize()
    record = book.find(name)
    message = 'Contact update successful'
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = 'Contact add successful'
    if phone:
        record.add_phone(phone)
    return message

@ input_error
def change_contact(args, book):
    '''Ця функція змінює номер телефону користувача в книзі'''
    name, old_phone, new_phone, *_ = args
    name = name.capitalize()
    message = 'Contact changed successful'
    if name not in book.data: # тут потрібно явно перевірити, інакше не працюватиме
        raise KeyError
    book.data[name].edit_phone(old_phone, new_phone)
    return message

@ input_error
def get_user_phone(args, book):
    '''Ця функція витягує номер користувача з книги'''
    name, *_ = args
    name = name.capitalize()
    if name in book.data:
        return [p.value for p in book.data[name].phones]
    raise KeyError

@input_error
def add_birthday(args, book):
    '''Додає дату народження до користувача'''
    name, birthday, *_ = args
    name = name.capitalize()
    message = 'Birthday added successful'
    if name not in book.data:
        raise KeyError
    book.data[name].add_birthday(birthday)
    return message

@input_error
def show_birthday(args, book):
    '''Повертає дату народження конкретного користувача'''
    name, *_ = args
    name = name.capitalize()
    if book.data[name].birthday is None:
        return 'Birthday doesn\'t added'
    return book.data[name].birthday.value

@input_error
def birthdays(book) -> list[Record]:
    '''Повертає всі дні народження протягом наступного тижня'''
    return book.get_upcoming_birthdays()
