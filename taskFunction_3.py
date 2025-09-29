import csv
from prettytable import PrettyTable, ALL
EXPERIENCE = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"
}

CURRENCY = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум"
}

russian_titles = ['№','Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии']

# +----------------------------------+
# +--------------------------+
# 

def formatter(row):
    formatted_row = {}

    formatted_row['Название:'] = row['name']
    formatted_row['Описание:'] = cut_by_100(row['description'].strip())
    skills = row['key_skills'].split('\n')
    formatted_row['Навыки:'] = cut_by_100(', '.join(skills) if skills else '')
    exp_id = row['experience_id']
    formatted_row['Опыт работы:'] = EXPERIENCE.get(exp_id, exp_id)
    premium = row['premium']
    formatted_row['Премиум-вакансия:'] = "Да" if premium.lower() == 'true' else "Нет"
    formatted_row['Компания:'] = row['employer_name']
    salary_from = row['salary_from']
    salary_to = row['salary_to']
    currency_code = row['salary_currency']
    gross = row['salary_gross']
    currency_name = CURRENCY.get(currency_code, currency_code)
    gross_text = "Без вычета налогов" if gross.lower() == 'true' else "С вычетом налогов"
    salary_str = f"{format_number(salary_from)} - {format_number(salary_to)} ({currency_name}) ({gross_text})"
    formatted_row['Оклад:'] = salary_str
    formatted_row['Название региона:'] = row['area_name']
    formatted_row['Дата публикации вакансии:'] = row['published_at']

    return formatted_row

def format_number(num_str):
    try:
        num = float(num_str)
        if num.is_integer():
            num = int(num)
            return f"{num:,}".replace(',', ' ')
        else:
            return f"{num:,.2f}".replace(',', ' ')
    except:
        return num_str

def cut_by_100(str):
    if len(str) > 100:
        return str[:100] + '...'

def print_vacancies(csv_file):
    table = PrettyTable()
    table.field_names = russian_titles
    table.align = "l"
    table.hrules = ALL
    for field in table.field_names:
        table.max_width[field] = 20
    
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        start = True
        for i, row in enumerate(reader, start=1):
            start = False
            formatted = formatter(row)
            desc = [i]
            for _ , r in formatted.items():
                desc.append(r)
            table.add_row(desc)
            print(table)
        if start:
            print("Нет данных")
filename = input()

if filename == '':
    filename = r'test\vacancies.csv'
else:
    filename = filename

# ulearn -- +---+----------------------+----------------------+----------------------+---------------+------------------+------------+----------------------+------------------+--------------------------+
# from test-+---+----------------------+----------------------+----------------------+--------------------+------------------+----------------------+----------------------+----------------------+--------------------------+  
# correct - +---+----------------------+----------------------+----------------------+--------------------+------------------+----------------------+----------------------+------------------+--------------------------+
#     +----------------------+----------------------+----------------------+----------------------
print_vacancies(filename)