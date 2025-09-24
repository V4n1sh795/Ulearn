import json
import bs4
import re

html = input()


exchange = {
    '₽': 1.0,
    '$': 100.0,
    '€': 105.0,
    '₸': 0.210,
    'Br': 30.0,
}
def currency(text):
    pattern = '|'.join(re.escape(symbol) for symbol in exchange.keys())
    match = re.search(pattern, text)
    return match.group() if match else None
def to_rubles(amount, currency):
    if currency not in exchange:
        raise ValueError(f"Неизвестная валюта: {currency}")
    
    return amount * exchange[currency]
result = {
    'vacancy': None,
    'salary': None,
    'experience': None,
    'company': None,
    'description': None,
    'skills': None,
    'created_at': None,
}

soup = bs4.BeautifulSoup(open(html), "html.parser")


vacancy_title = soup.find(class_='vacancy-title')
salary = vacancy_title.find(attrs={"data-qa": 'vacancy-salary'})
salary_tile = salary.find(class_='bloko-header-section-2 bloko-header-section-2_lite')
aaaaaaaaaaaaaaaaa = re.findall(r'<!--\s*-->\s*([\d\s]+?)\s*<!--\s*-->', str(salary_tile))
curr = currency(str(salary_tile))
salary =[x.replace('\xa0', '') for x in aaaaaaaaaaaaaaaaa]
if len(salary) == 1:
    result['salary'] = str(to_rubles(float(''.join(salary)), curr))
else:
    result['salary'] = f"{to_rubles(float(salary[0]), curr)}->{to_rubles(float(salary[1]), curr)}"
result['vacancy'] = vacancy_title.find('h1').text

vacancy_description_list_item = soup.find(class_='vacancy-description-list-item').text
exp = re.findall(r'(\d+)–(\d+)', vacancy_description_list_item) # [['1', '3']]
try:
    result['experience'] = f'{exp[0][0]}-{exp[0][1]}'
except Exception as e:
    result['experience'] = None
vacancy_company_name = soup.find(class_="vacancy-company-name").text
result['company'] = vacancy_company_name

description_element = soup.find(attrs={"data-qa": "vacancy-description"}).text
result['description'] = description_element

all_desc = soup.find_all(class_='vacancy-description')
for desc in all_desc:
    try:
        key_skills = desc.find_all(class_='vacancy-section')
    except Exception as e:
        continue
span_skills = [x for x in key_skills][2].find_all('span')
result['skills'] = '; '.join([x.text for x in span_skills])

date = soup.find(class_='vacancy-creation-time-redesigned').text
result['created_at'] = re.search(r'\d.*\d', date).group().replace('\xa0', ' ')
print(json.dumps(result))
