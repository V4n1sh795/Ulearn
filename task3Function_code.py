import csv
from prettytable import PrettyTable, ALL
import re
from datetime import datetime

transforner = {
    'Нет опыта': 0,
    'От 1 года до 3 лет': 1,
    'От 3 до 6 лет': 2,
    'Более 6 лет': 3
}
full_key_list = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад", "Название региона", "Дата публикации вакансии"] 

def fix_lenght(key_list):
    res = []
    for elem in key_list:
        res.append(elem.ljust(20))
    return res


def cut_by_100(str):
    if len(str) > 100:
        return str[:100] + '...'
    else:
        return str

def sort_table(table): # PrettyTableObj
    global reversed_or_not
    global full_key_list
    def sort_param(row): # row = [[vac], [desc], [skills], ... ]
        global field_to_sort
        global transforner
        if field_to_sort == 'Оклад':
            str1 = row[6]
            salary = [int(x.replace(' ', '')) for x in ''.join(re.findall(r'[\d\s]+-\s*[\d\s]+', str1)).split('-')]
            return salary[1]
        
        elif field_to_sort == 'Опыт работы':
            return transforner[row[3]]
        
        elif field_to_sort == 'Дата публикации вакансии':
            date_str = row[8]
            return datetime.strptime(date_str, "%H:%M:%S %d/%m/%Y")
        
    new_table = PrettyTable()
    rows = table.rows
    new_table.align = "l"
    new_table.hrules = ALL
    new_table.field_names = ['№'] + full_key_list
    for field in new_table.field_names:
        new_table.max_width[field] = 20
    sorted_rows = sorted(rows, reverse=reversed_or_not, key=sort_param)
    for i, row in enumerate(sorted_rows, start=1):
        new_table.add_row([i] + row)
    return new_table

def numerate_table(table): # PrettyTableObj
    new_table = PrettyTable()
    rows = table.rows
    new_table.align = "l"
    new_table.hrules = ALL
    new_table.field_names = ['№'] + full_key_list
    for field in new_table.field_names:
        new_table.max_width[field] = 20
    for i, row in enumerate(rows, start=1):
        new_table.add_row([i] + row)
    return new_table
def procces_row(row): # dict like {name: param,  ...}
    add_row = [cut_by_100(value) for key, value in row.items()]
    def acces_filter():
        global filt # <- [Навыки, CSS]
        def if_salary(add_row):
            if filt[0] == 'Оклад':
                str = row['Оклад']
                salary = [int(x.replace(' ', '')) for x in ''.join(re.findall(r'[\d\s]+-\s*[\d\s]+', str)).split('-')]
                if salary[0] <= int(filt[1]) <= salary[1]:
                    return add_row
                else:
                    None
            elif filt[0] == 'Идентификатор валюты оклада':
                str = row['Оклад']
                currency_match = re.search(r'\(([^)]+)\)', str)
                currency = currency_match.group(1).strip() if currency_match else None
                if currency == filt[1]:
                    return add_row
                else:
                    return None
            
            else:
                return add_row # if_salary
        if filt == ['']:
            return add_row # acces_filter
        elif filt[0] in ['Оклад', 'Идентификатор валюты оклада']:
            return if_salary(add_row)
        elif filt[1] in row[filt[0]]:
            return add_row # acces_filter  
        else:
            return None
    return acces_filter()


# def processing_value(value, key):
    # def in_filter():
    #     global filt
    #     if filt[0] == key:
    #         if filt[1] in value:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return cut_by_100(value)
#     if in_filter == True:
#         return cut_by_100(value)
#     else: 
#         return None

def create_row_generator(fn):
    with open(fn, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            yield [i, row]

def print_table(gen, start_row, last_row, key_list):
    global full_key_list
    global field_to_sort
    table = PrettyTable()
    table.field_names = full_key_list
    table.align = "l"
    table.hrules = ALL
    for field in table.field_names:
        table.max_width[field] = 20
    try:
        while True:
            _, row = next(gen)        
            # add_row = [i] + [processing_value(value, key) for key, value in row.items()]
            if procces_row(row):
                add_row = procces_row(row)
                table.add_row(add_row)
            else:
                continue
    except StopIteration:
        pass
    if field_to_sort != '':
        table = sort_table(table)
    else: 
        table= numerate_table(table=table)
        pass
    res = table.get_string(start=start_row-1, end=last_row, fields=['№'] + key_list)
    print(res)
            

fn = input() # filename
if fn:
    fn = fn
else:
    fn = "test/vacancies_for_functional.csv"

gen = create_row_generator(fn)

filt = [x.strip() for x in input().split(':')] # filter

field_to_sort = input()

reversed_or_not = True if input() == 'Да' else False

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

if key_list != ['']: #key_skills
    key_list = key_list
else:
    key_list = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад", "Название региона", "Дата публикации вакансии"] 

print_table(gen,first_row, last_row, key_list)




