import csv

filename = input()
russian_titles = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания', 'Нижняя граница вилки оклада', 'Верхняя граница вилки оклада', 'Оклад указан до вычета налогов', 'Идентификатор валюты оклада', 'Название региона', 'Дата и время публикации вакансии']

TrueFalse_replace_list = ['Премиум-вакансия', 'Оклад указан до вычета налогов',]

if filename == '':
    filename = r'test\vacancies.csv'
else:
    filename = filename
def clean(r, h):
    if '\n' in r:
        return r.replace('\n', ', ').strip()
    if 'True' in r and h in TrueFalse_replace_list:
        return r.replace('True', 'Да').strip()
    if 'False' in r and h in TrueFalse_replace_list:
        return r.replace('False', 'Нет').strip()
    # if '&quot' in r:
    #     return r.replace('&quot;', '"')
    else:
        return r.strip()
    
def csv_reader(filename):
    res = []
    with open(filename, encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        head = next(reader)
        for row in reader:
            res.append(row)
        return [head, res]
def print_vacancies(rows, titels):
    for row in rows:
        for h, r in zip(titels, row):
            print(f"{h}: {clean(r, h)}")
        if row != rows[-1]:
            print()
        else:
            continue
titles, rows = csv_reader(filename)
print_vacancies(rows, russian_titles)
