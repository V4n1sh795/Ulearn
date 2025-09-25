import json
import re

import bs4

html = input()

exchange = {
    '₽': 1.0,
    '$': 100.0,
    '€': 105.0,
    '₸': 0.210,
    'Br': 30.0,
}

result = {
    'vacancy': None,
    'salary': None,
    'experience': None,
    'company': None,
    'description': None,
    'skills': None,
    'created_at': None,
}

def currency(digital, cur):
    match cur:
        case '₽':
            return str(float(digital))
        case '$':
            return str(float(digital)*exchange['$'])
        case '€':
            return str(float(digital)*exchange['€'])
        case '₸':
            return str(float(digital)*exchange['₸'])
        case 'Br':
            return str(float(digital)*exchange['Br'])
def salary(text):
    ph = (re.findall(r'\d*.*?\d\s[₽$€₸B][r]{0,1}', text))[0].replace(' ','').replace('\xa0','')
    cur = (re.findall(r'[₽$€₸B][r]{0,1}', text))[0]
    while ('₽' == ph[-1:]) or ('$' == ph[-1:]) or ('€' == ph[-1:]) or ('₸' == ph[-1:]) or ('B' == ph[-1:]) or ('r' == ph[-1:]):
        ph = ph[:-1]
    if 'до' == ph[:2] or ('от' == ph[:2] and not('до' in ph)):
        ph = ph.replace('до', '').replace('от', '')
        return currency(ph, cur)
    else:
        ph = ph.split('до')
        ph[0] = currency(ph[0].replace('от', ''), cur)
        ph[1] = currency(ph[1], cur)
        return f'{ph[0]}->{ph[1]}'

def expirience(text):
     text = re.findall(r'\d+', text)
     if len(text) == 2:
         return f'{text[0]}-{text[1]}'
     elif len(text) == 1:
         return text[0]
     else:
         return None

def skills(vacancy_section):
    skill = 'ниче не нашло'
    for i in vacancy_section:
        try:
            skill = i.find_all(class_='vacancy-section')
        except:
            continue
    skill = [x for x in skill][2].find_all('span')
    return '; '.join([x.text for x in skill])

def created_at(vacancy_creation_time_redesigned):
    return str(((re.findall(r'[123]?\d\s\D+\s\d{4}', vacancy_creation_time_redesigned))[0]).replace('\xa0',' '))

bs = bs4.BeautifulSoup(open(html), "html.parser")
vacancy = str(bs.find('h1', class_='bloko-header-section-1', attrs={"data-qa": "vacancy-title"}).text)
sal = str((bs.find(attrs={"data-qa": "vacancy-salary"}).text))
exp = str((bs.find(class_='vacancy-description-list-item').text))
comp = str((bs.find(class_='vacancy-company-name')).text)
descrip = str((bs.find(attrs={"data-qa": "vacancy-description"})).text)
vacancy_section = bs.find_all(class_='vacancy-description')
vacancy_creation_time_redesigne = str((bs.find(class_='vacancy-creation-time-redesigned')).text)

result['vacancy'] = vacancy
result['salary'] = salary(sal)
result['experience'] = expirience(exp)
result['company'] = comp
result['description'] = descrip
result['skills'] = skills(vacancy_section)
result['created_at'] = created_at(vacancy_creation_time_redesigne)
print(json.dumps(result))

