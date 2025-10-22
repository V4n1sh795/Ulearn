from var_dump import var_dump
import csv
import re
# main class - Vacancy and sec is Salary 
# vacancy => vacancy::name, ..., vacancy::Salary::salary_from

class Vacancy:
    def __init__(self, row):
        self.name = row.get('Название')
        self.description = row.get('Описание')
        self.key_skills = row.get('Навыки')
        self.experience_id = row.get('Опыт работы')
        self.premium = row.get('Премиум-вакансия')
        self.employer_name = row.get('Компания')
        sal = row.get('Оклад')
        self.salary = Salary(sal)
        self.area_name = row.get('Название региона')
        self.published_at = row.get('Дата публикации вакансии')



class Salary:   
    def __init__(self, str):
        # print(str)
        salary = [x.replace(' ', '') for x in ''.join(re.findall(r'[\d\s]+-\s*[\d\s]+', str)).split('-')]
        currency_match = re.findall(r'\(([^)]+)\)', str)
        # print(salary)
        # print(currency_match)
        self.salary_from = salary[0]
        try:
            self.salary_to = salary[1]
        except IndexError:
            self.salary_to = salary[0]
        self.salary_gross = currency_match[0]
        self.salary_currency = currency_match[1]
        
        # self.salary_gross = str.split(" ").remove(self.salary_currency, self.salary_from, self.salary_to)
        


def process_row():
    pass

def open_file():
    fn = input()
    if fn:
        fn = fn
    else:
        fn = "test/vacancies_for_functional.csv"
    return fn

def create_row_generator(fn):
    with open(fn, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            yield [i, row]
def main():
    main_list = []
    filename = open_file()
    gen = create_row_generator(filename)
    try:
        while True:
            _, row = next(gen)
            v = Vacancy(row)
            main_list.append(v)
    except StopIteration:
        pass
    var_dump(main_list)
    


if __name__ == '__main__':
    main()