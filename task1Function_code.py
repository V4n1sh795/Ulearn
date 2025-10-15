
import csv
from prettytable import PrettyTable, ALL

full_key_list = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад", "Название региона", "Дата публикации вакансии"]

# def fix_lenght(key_list):
#     res = []
#     for elem in key_list:
#         res.append(elem.ljust(20))
#     return res

def cut_by_100(str):
    if len(str) > 100:
        return (str[:100] + '...')
    else:    
        return str

def create_row_generator(fn):
    with open(fn, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            yield [i, row]

def print_table(gen, start_row, last_row, key_list):
    global full_key_list
    table = PrettyTable()
    table.field_names = ['№'] + full_key_list
    table.align = "l"
    table.hrules = ALL
    for field in table.field_names:
        table.max_width[field] = 20
    try:
        while True:
            i, row = next(gen)        
            add_row = [i] + [cut_by_100(value) for key, value in row.items()]
            table.add_row(add_row)
    except StopIteration:
        pass
    res = table.get_string(start=start_row-1, end=last_row, fields=['№'] + key_list)
    print(res)
            



fn = input()
if fn:
    fn = fn
else:
    fn = "test/vacancies_for_functional.csv"

gen = create_row_generator(fn)


accepted_list = input().split()
if accepted_list == []:
    first_row = 1
    last_row = 10**10
elif len(accepted_list) == 1:
    first_row = int(accepted_list[0])
    last_row = 10**10
else:
    first_row = int(accepted_list[0])
    last_row = int(accepted_list[1])
key_list = input().split(', ')

if key_list != ['']:
    key_list = key_list
else:
    key_list = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад", "Название региона", "Дата публикации вакансии"] 

print_table(gen,first_row, last_row, key_list)




