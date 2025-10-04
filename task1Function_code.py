import csv
from prettytable import PrettyTable, ALL

def fix_lenght(key_list):
    res = []
    for elem in key_list:
        res.append(elem.ljust(20))
    return res

def create_row_generator(fn):
    with open(fn, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            yield [i, row]

def print_table(gen, start_row, last_row, key_list):
    table = PrettyTable()
    table.field_names = ['№'] + key_list
    table.align = "l"
    table.hrules = ALL
    for field in table.field_names:
        table.max_width[field] = 20
#    def only_in_keys(row):
#        right_row = {}
#        for (key, value) in row.items():
#            if key in key_list:
#                right_row[key] = value
#        return right_row
    try:
        while True:
            i, row = next(gen)
            if i in range(start_row, last_row+1):
                add_row = [i] + [value for key, value in row.items() if key in key_list]
                table.add_row(add_row)
            if i > last_row:
                break
    except StopIteration:
        pass
    print(table)
            



fn = input()
if fn:
    fn = fn
else:
    fn = "test/vacancies_for_functional.csv"
gen = create_row_generator(fn)
try:
    first_row, last_row = map(int, input().split())
except ValueError:
    try:
        first_row = first_row
    except NameError:
        first_row = 1
    try:
        last_row = last_row
    except NameError:
        last_row = 10 ** 10

key_list = input().split()
if key_list:
    key_list = key_list
else:
    key_list = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад", "Название региона", "Дата публикации вакансии"] 


print_table(gen,first_row, last_row, key_list)




