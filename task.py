# Задача №49. Решение в группах
# Создать телефонный справочник с
# возможностью импорта и экспорта данных в
# формате .txt. Фамилия, имя, отчество, номер
# телефона - данные, которые должны находиться
# в файле.
# 1. Программа должна выводить данные
# 2. Программа должна сохранять данные в
# текстовом файле
# 3. Пользователь может ввести одну из
# характеристик для поиска определенной
# записи(Например имя или фамилию
# человека)
# 4. Использование функций. Ваша программа
# не должна быть линейной

# Дополнить справочник возможностью копирования данных
# из одного файла в другой. Пользователь вводит номер строки,
# которую необходимо перенести из одного файла в другой.

from csv import DictReader, DictWriter

from os.path import exists
 
class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt

def get_info():
    is_valid = False
    first_name = None
    while not is_valid:
        first_name = input('Введи имя: ')
        if len(first_name) == 0:
            print('Не ввели имя!')
        else:
            is_valid = True
    is_valid = False
    last_name = None
    while not is_valid:
        last_name = input('Введи фамилию: ')
        if len(last_name) == 0:
            print('Не ввели фамилию!')
        else:
            is_valid = True
    phone_number = None
    is_valid = False
    while not is_valid:
        try:
            phone_number = input('Введите номер телефона: ')
            if not phone_number.isnumeric():
                raise ValueError
            if len(str(phone_number)) != 11:
                raise LenNumberError('Неверная длина номера!')
            else:
                is_valid = True
        except ValueError:
            print('Невалидный номер')
        except LenNumberError as err:
            print(err)
    info = [first_name, last_name, phone_number]
    return info

def create_file(f_name):
    with open(f_name, 'w', encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()

def write_file(lst, f_name):
    with open(f_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        res = list(f_reader)
    for el in res:
        if str(lst[2]) == el['Телефон']:
            print('Такой телефон уже есть')
            return
    obj = {'Имя': lst[0], 'Фамилия': lst[1], 'Телефон': lst[2]}
    with open(f_name, 'w', encoding='utf-8', newline='') as data:
        res.append(obj)
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)

def read_file(f_name):
    with open(f_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)

def find_some_rows(some_key, some_str):
    if not exists(file_name):
        print('Нет файла')
        return
    lst = read_file(file_name)
    res = []
    for el in lst:
        if el[some_key].lower() == some_str.lower():
            res.append(el)
    if len(res) > 0:
        return res
    else:
        return 'Ничего не найдено!'

def copy_row_to_file(f_name, is_append=False):
    if not exists(f_name):
                print('Нет файла')
                return
    lst = read_file(f_name)
    file_name_to_copy = input('Введите имя файла: ')
    if file_name_to_copy[len(file_name_to_copy) - 4:] != '.csv':
        file_name_to_copy += '.csv'
    if not exists(file_name_to_copy):
        create_file(file_name_to_copy)
        is_append = False
    is_valid = False
    row_number = None
    while not is_valid:
        try:
            row_number = int(input('Введите номер копируемой строки: '))
            if row_number > len(lst) or row_number < 1:
                raise LenNumberError(
                    'Введенный номер строки не существует в файле!')
            is_valid = True
        except ValueError:
            print('Невалидный номер строки')
        except LenNumberError as err:
            print(err)
    rows = []
    if is_append: 
        with open(file_name_to_copy, 'r', encoding='utf-8') as data:
            f_reader = DictReader(data)
            rows = list(f_reader)
    with open(file_name_to_copy, 'w', encoding='utf-8', newline='') as data:
        rows.append(lst[row_number - 1])
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(rows)

def main():
    file_name = input('Ведите имя файла справочника без расширения: ')
    if len(file_name) == 0:
        print('Пустое имя файла. Будет использовано имя по умолчанию(phones.csv).')
        file_name = 'phones.csv'
    else:
        file_name = file_name + '.csv'
    while True:
        command = input('Введите команду (список команд - ? ): ')
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(get_info(), file_name)
        elif command == 'r':
            if not exists(file_name):
                print('Нет файла')
                continue
            print(*read_file(file_name))
        elif command == 'c -a':
            copy_row_to_file(file_name, True)
        elif command == 'c':
            copy_row_to_file(file_name)
        elif command == 'f':
            while True:
                command = input(
                    'Введите характеристику для поиска(fn - имя, ln - фамилия, tel - номер телефона, b - вернуться обратно): ')
                if command == 'b':
                    break
                elif command == 'ln':
                    find_text = input('Найти по фамилии: ')
                    print(*find_some_rows('Фамилия', find_text))
                elif command == 'fn':
                    find_text = input('Найти по имени: ')
                    print(*find_some_rows('Имя', find_text))
                elif command == 'tel':
                    find_text = input('Найти по номеру телефона: ')
                    print(*find_some_rows('Телефон', find_text))
                else:
                    print('Неверная команда!')
                    continue
        elif command == 'clear':
            create_file(file_name)
        elif command == '?' or command.lower() == 'help':
            print('Команды:')
            print('q - выход')
            print('f - поиск')
            print('w - добавить строку в файл справочника')
            print('r - вывести содержимое файла справочника')
            print('c - скопировать строку справочника в другой файл с перезаписью')
            print('c -a - скопировать строку справочника в другой файл с сохранением данных')
            print('clear - очистить текущий файл справочника')
        else:
            print('Неверная команда!')
            continue

main()