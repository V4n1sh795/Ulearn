import csv
import re
import math

def sklon(n, n1, n2_4, n5_0):
    n = abs(n) % 100
    if 11 <= n <= 19:
        return n5_0
    last_digit = n % 10
    if last_digit == 1:
        return n1
    elif last_digit in (2, 3, 4):
        return n2_4
    else:
        return n5_0

def clean(r):
    if r is None:
        return "Нет данных"
    if '\n' in r:
        cleaned_lines = []
        for line in r.split('\n'):
            cleaned_line = re.sub(r'<[^>]+>', '', line).strip()
            cleaned_line = re.sub(r'\s+', ' ', cleaned_line)
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
        return ';'.join(cleaned_lines)
    else:
        cleaned = re.sub(r'<[^>]+>', '', r).strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned if cleaned else "Нет данных"

def del_trash(list):
    res = list.copy()
    trash_list = ['description', 'experience_id', 'premium', 'salary_gross', 'published_at']
    for trash in trash_list:
        if trash in res:
            del res[trash]
    return res

filename = input()
res = []
valid_rows = []

with open(filename, encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    head = next(reader)
    half_head = round(len(head) / 2)
    
    for row in reader:
        if len([x for x in row if x != '']) >= half_head:
            row_data = {}
            for h, r in zip(head, row):
                row_data[h] = clean(r)
            
            filtred_data = del_trash(row_data)
            
            if filtred_data.get('salary_currency') != "RUR":
                continue
            
            salary_from_str = filtred_data.get('salary_from', '')
            salary_to_str = filtred_data.get('salary_to', '')
            
            from_val = 0
            to_val = 0
            
            if salary_from_str and salary_from_str != "Нет данных":
                try:
                    from_val = float(salary_from_str)
                except (ValueError, TypeError):
                    from_val = 0
                    
            if salary_to_str and salary_to_str != "Нет данных":
                try:
                    to_val = float(salary_to_str)
                except (ValueError, TypeError):
                    to_val = 0
                
            average_salary = int(from_val+to_val) // 2

            try:
                skills_str = filtred_data.get('key_skills', '')
                if skills_str == "Нет данных" or not skills_str:
                    skills_list = []
                else:
                    skills_list = [skill.strip() for skill in skills_str.split(';') if skill.strip()]
                
                cash = {
                    'company': filtred_data.get('employer_name', 'Нет данных'), 
                    'name': filtred_data.get('name', 'Нет данных'), 
                    'area': filtred_data.get('area_name', 'Нет данных'), 
                    'salary': average_salary, 
                    'is_ru': filtred_data.get('salary_currency', 'Нет данных'),
                    'skills': skills_list
                }
                res.append(cash)
            except Exception as e:
                continue

total_rur_vacancies = len(res)

one_percent_threshold = math.floor(total_rur_vacancies * 0.01)

skills = {}
for r in res:
    for skill in r['skills']:
        if skill:
            skills[skill] = skills.get(skill, 0) + 1

city = {}
for vacancy in res:
    area_name = vacancy['area']
    salary = vacancy['salary']
    
    if area_name not in city:
        city[area_name] = {'salaries': [], 'count': 0}
    
    city[area_name]['salaries'].append(salary)
    city[area_name]['count'] += 1

filtered_city = {}
for city_name, data in city.items():
    if data['count'] >= one_percent_threshold:
        if data['salaries']:
            avg_salary = sum(data['salaries']) // len(data['salaries'])
        else:
            avg_salary = 0
        filtered_city[city_name] = [avg_salary, data['count']]

print('Самые высокие зарплаты:')
i = 0
for sallary_tile in sorted(res, key=lambda x: x['salary'], reverse=True)[:10]:
    i += 1
    name = sallary_tile['name']
    company = sallary_tile['company']
    sallary = sallary_tile['salary']
    area = sallary_tile['area']
    rub = sklon(sallary, 'рубль','рубля','рублей')
    print(f'    {i}) {name} в компании "{company}" - {sallary} {rub} (г. {area})')
print()

i=0
print('Самые низкие зарплаты:')
for sallary_tile in sorted(res, key=lambda x: x['salary'], reverse=False)[:10]:
    i += 1
    name = sallary_tile['name']
    company = sallary_tile['company']
    sallary = sallary_tile['salary']
    area = sallary_tile['area']
    rub = sklon(sallary, 'рубль','рубля','рублей')
    print(f'    {i}) {name} в компании "{company}" - {sallary} {rub} (г. {area})')
print()

num_skills = len(skills)
if num_skills % 10 == 1 and num_skills % 100 != 11:
    sk = 'скилл'
else:
    sk = 'скиллов'

print(f'Из {num_skills} {sk}, самыми популярными являются:')
i = 0
for skill in sorted(skills.items(), key=lambda x: x[1], reverse=True)[:10]:
    i += 1
    count = skill[1]
    times = sklon(count, 'раз', 'раза', 'раз')
    print(f"    {i}) {skill[0]} - упоминается {count} {times}")
print()

num_filtered_cities = len(city)
if num_filtered_cities % 10 == 1 and num_filtered_cities % 100 != 11:
    city_word = 'города'
else:
    city_word = 'городов'

print(f'Из {num_filtered_cities} {city_word}, самые высокие средние ЗП:')
i = 0
for c in sorted(filtered_city.items(), key=lambda x: x[1][0], reverse=True)[:10]:
    i += 1
    city_name = c[0]
    avg_salary = c[1][0]
    vacancies_count = c[1][1]
    vac_word = sklon(vacancies_count, 'вакансия', 'вакансии', 'вакансий')
    rub = sklon(avg_salary, 'рубль','рубля','рублей')
    print(f"    {i}) {city_name} - средняя зарплата {avg_salary} {rub} ({vacancies_count} {vac_word})")