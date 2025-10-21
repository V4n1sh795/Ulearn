from var_dump import var_dump
import csv
import re
# main class - Vacancy and sec is Salary 
# vacancy => vacancy::name, ..., vacancy::Salary::salary_from

class Vacancy:
    def __init__(self, row):
        self.name = row[0]
        self.description = row[1]
        self.key_skills = row[2]
        self.experience_id = row[3]
        self.premium = row[4]
        self.employer_name = row[5]
        self.salary = Salary(row[6])
        self.area_name = row[7]
        self.published_at = row[0]



class Salary:   
    def __init__(self, str):
        salary = [x.replace(' ', '') for x in ''.join(re.findall(r'[\d\s]+-\s*[\d\s]+', str)).split('-')]
        currency_match = re.findall(r'\(([^)]+)\)', str)
        self.salary_from = salary[0]
        self.salary_to = salary[1]
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
    with open(fn, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
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