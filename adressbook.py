'''Контактна книга'''

from collections import UserDict
from datetime import datetime


class Field:
    '''Клас створений для того щоб інші класи записи могли наслідуватись від нього
    він фактично просто зберігає змінну під назвою value, обидва класи матимуть цю
    змінну, це зроблено для того щоб у випадку якщо потрібно змінити логіку цієї
    змінної то не змінювати в кожному класі по окремо'''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    '''Даний клас наразі немає жодних методів чи якихось власних полів, його завдання
    просто бути об'єктом який зберігатиме 1 змінну отриману від Field'''
    pass

class Phone(Field):
    '''Даний клас перевіряє при ініціалізації чи номер телефону відповідає відповідній
    валідації а саме 10 знакам, якщо не відповідає то викидає помилку, ми можемо додати
    більше перевірок згодом, наприклад на те чи це дійсно цифри, чи якось перехоплювати
    помилки'''
    def __init__(self, phone):
        if len(phone) == 10 and phone.isdigit():
            super().__init__(phone)
        else:
            raise ValueError('Length of phone must be equal 10, and be int type')

class Birthday(Field):
    '''Даний клас записує та запам'ятовує дату народження користувача, яка потім
    використовуватиметься для того щоб знати коли його привітати'''
    def __init__(self, value):
        try:
            value = datetime.strptime(value, '%d.%m.%Y').date()
            super().__init__(value)
        except ValueError as e:
            raise ValueError('Invalid date format. Use DD.MM.YYYY') from e

class Record:
    '''Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.'''
    def __init__(self, nam: str):
        self.name = Name(nam)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}\
, birthday: {self.birthday}"

    def add_phone(self, phone: str):
        '''Метод додає номер телефону'''
        for i in self.phones:
            if phone == i.value:
                raise ValueError('Phone number already exist, try another')
        obj_phone = Phone(phone)
        self.phones.append(obj_phone)

    def edit_phone(self, old_phone: str, new_phone: str):
        '''Знаходить старий номер телефону і замінює його на новий'''
        for phone in self.phones:
            if phone.value == old_phone and new_phone != phone.value:
                phone.value = new_phone
            else:
                raise ValueError('New phone number already exist, try another')

    def find_phone(self, phone: str) -> Phone:
        '''Шукає номер телефону і повертає його'''
        for p in self.phones:
            if p.value == phone:
                return p

    def add_birthday(self, birthday: str):
        '''Додає об'єкт дня народження в поле birthday'''
        self.birthday = Birthday(birthday)

class AddressBook(UserDict):
    '''Клас для зберігання та управління записами.'''
    def add_record(self, rec: Record):
        '''додає запис до адресної книги'''
        self.data[rec.name.value] = rec # тут важливо записати саме об'єкт, а не його значення

    def find(self, nam: str) -> list[Phone]:
        '''Шукає користувача за іменем та повертає його записи'''
        return self.data.get(nam)

    def delete(self, nam: str):
        '''Видаляє користувача за іменем'''
        self.data.pop(nam)

    def get_upcoming_birthdays(self) -> list[(Record, datetime.date)]:
        '''Виводить список користувачів у яких день народження протягом наступного
        тижня"'''
        congratulations = list()
        current_date = datetime.today().date()
        for user in self.data.values():
            if user.birthday is None:
                continue
            temp = user.birthday.value.replace(year=current_date.year)
            differ = temp - current_date
            if 0 <= differ.days <= 7:
                congratulations.append((user, temp))
        return congratulations
