from var_dump import var_dump
import csv
import re
# main class - Vacancy and sec is Salary 
# vacancy => vacancy::name, ..., vacancy::Salary::salary_from

class Vacancy:
    def __init__(self, row):
        # print(row)
        self.name = row.get('name')
        self.description = row.get('description')
        self.key_skills = row.get('key_skills')
        self.experience_id = row.get('experience_id')
        self.premium = row.get('premium')
        self.employer_name = row.get('employer_name')
        self.salary = Salary([row.get('salary_from'), row.get('salary_to'), row.get('salary_gross'), row.get('salary_currency')])
        self.area_name = row.get('area_name')
        self.published_at = row.get('published_at')



class Salary:   
    def __init__(self, salary):
        self.salary_from = salary[0]
        self.salary_to = salary[1]
        self.salary_gross = salary[2]
        self.salary_currency = salary[3]
        
        # self.salary_gross = str.split(" ").remove(self.salary_currency, self.salary_from, self.salary_to)
        


def process_row():
    pass

def open_file():
    fn = input()
    if fn:
        fn = fn
    else:
        fn = "test/small_vac_50.csv"
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