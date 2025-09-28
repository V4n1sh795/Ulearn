import csv

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

def formatter(row):
    formatted_row = {}

    formatted_row['Название:'] = row['name']
    formatted_row['Описание:'] = row['description'].strip()
    skills = row['key_skills'].split('\n')
    formatted_row['Навыки:'] = ', '.join(skills) if skills else ''
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

def last_item(csv_file):
    with open(csv_file, encoding='utf-8') as file:
        reader = list(csv.DictReader(file))
    return reader[-1]

def print_vacancies(csv_file):
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            formatted = formatter(row)
            for t, r in formatted.items():
                print(f'{t} {r}')
            if row == last_item(csv_file):
                continue
            else:
                print()
filename = input()

if filename == '':
    filename = r'test\vacancies.csv'
else:
    filename = filename

print_vacancies(filename)