import csv
from datetime import datetime

#изменить в словаре года из строки в числа 
#отрефокторить сортировку
correct = {2003: 81875, 2005: 106000, 2006: 86700, 2007: 100367, 2008: 107500, 2009: 54962, 2010: 85000, 2011: 120000, 2012: 22600, 2013: 75225, 2014: 203774, 2015: 55000, 2016: 105504, 2019: 72500, 2020: 88833, 2022: 78547, 2023: 97500, 2024: 100495}
currency_to_rub = {
    "Манаты": 35.68,
    "Белорусские рубли": 23.91,
    "Евро": 59.90,
    "Грузинский лари": 21.74,
    "Киргизский сом": 0.76,
    "Тенге": 0.13,
    "Рубли": 1,
    "Гривны": 1.64,
    "Доллары": 60.66,
    "Узбекский сум": 0.0055,
}

class DataSet:
    res = []
    def __init__(self, filename):
        fn = filename
        if fn:
            fn = fn
        else:
            fn = "test/small_vac_50.csv"
        with open(fn, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
               self.res.append(row)
    
class Statistics:
    def __init__(self, dataset):
        
        self.middle_salary = Utils.create_static_table(dataset)
        self.vacancy_num = Utils.create_static_table(dataset)
        self.middle_salary_for = Utils.create_static_table(dataset)
        self.vacancy_num_for = Utils.create_static_table(dataset)
        self.middle_salary_in = Utils.create_city_table(dataset)
        self.vacancy_part_in = Utils.create_city_table(dataset)
        checker = []
        for row in dataset:
            
            year = Utils.getyear(row)
            city = Utils.getcity(row)
            middle_salary = Utils.middle_salary(row)
            
            self.vacancy_num[year] += 1
            self.middle_salary[year] += middle_salary
            self.vacancy_part_in[city] += 1
            self.middle_salary_in[city] += middle_salary
            if year == 2009 or year == 2014 or year == 2016 or year == 2022 or year == 2005:
                checker.append([year, row['salary_from'], row['salary_to'], row['salary_currency']])
            if Utils.nameIN(row):
                self.middle_salary_for[year] += int(middle_salary)
                self.vacancy_num_for[year] += 1
        
        for y, _ in self.middle_salary.items():
            try:
                self.middle_salary[y] = round(self.middle_salary[y] / self.vacancy_num[y])
            except ZeroDivisionError:
                del self.middle_salary[y]
        
        for y, _ in self.middle_salary.items():
            try:
                self.middle_salary_for[y] = round(self.middle_salary_for[y] / self.vacancy_num_for[y])
            except ZeroDivisionError:
                del self.middle_salary_for[y]

        for c, _ in self.middle_salary_in.items():
            try:
                self.middle_salary_in[c] = round(self.middle_salary_in[c] / self.vacancy_part_in[c])
            except ZeroDivisionError:
                del self.middle_salary_in[c]

        for c, _ in self.vacancy_part_in.items():
            try:
                self.vacancy_part_in[c] = self.vacancy_part_in[c] / len(dataset)
            except ZeroDivisionError:
                del self.vacancy_part_in[c]

        self.middle_salary = Utils.clear_and_sort_nums(self.middle_salary, False)
        self.vacancy_num = Utils.clear_and_sort_nums(self.vacancy_num, False)
        self.middle_salary_for = Utils.clear_and_sort_nums(self.middle_salary_for, False)
        self.vacancy_num_for = Utils.clear_and_sort_nums(self.vacancy_num_for, False)
        self.middle_salary_in = Utils.clear_and_sort_nums(self.middle_salary_in, False)
        self.vacancy_part_in = Utils.clear_and_sort_nums(self.vacancy_part_in, True)
        for elem in sorted(checker, key = lambda x: x[0]):
            print(elem)
        # print('Средняя зарплата по годам:', self.middle_salary)
        # print('Количество вакансий по годам:', self.vacancy_num)
        # print("Средняя зарплата по годам для профессии 'разработчик':", self.middle_salary_for)
        # print("Количество вакансий по годам для профессии 'разработчик':", self.vacancy_num_for)
        # print('Средняя зарплата по городам:', self.middle_salary_in)
        # print('Доля вакансий по городам:', self.vacancy_part_in)
class Utils:
    @staticmethod
    def getyear(row):
        return int(row['published_at'][-4:])
    @staticmethod
    def middle_salary(row):
        s_from = int(row['salary_from'])
        s_to = int(row['salary_to'])
        currency = row['salary_currency']
        
        if currency != 'Рубли':
            global currency_to_rub
            rate = int(currency_to_rub[currency])
            s_from *= rate
            s_to *= rate
    
        return round((s_from + s_to) / 2)
    @staticmethod
    def nameIN(row):
        global checked_name
        name = row.get('name', '')
        if not isinstance(name, str):
            name = str(name)
        return checked_name.lower() in name.lower()
    
    @staticmethod
    def create_static_table(dataset):
        table = {}
        for row in dataset:
            table[Utils.getyear(row)] = 0
        return table
    
    @staticmethod
    def create_city_table(dataset):
        table = {}
        for row in dataset:
            table[Utils.getcity(row)] = 0
        return table
    
    @staticmethod
    def getcity(row):
        return row['area_name']
    
    @staticmethod 
    def clear_and_sort_nums(dict1, reverse):
        res = dict(sorted(dict1.items(), key=lambda item: item[0], reverse=reverse))
        # return [value for _, value in res.items() if value != 0]\
        return res
    @staticmethod 
    def clear_and_sort_citys(dict1, reverse):
        res = dict(sorted(dict1.items(), key=lambda item: item[1], reverse=reverse))
        # return [key: value for key, value in res.items() if value != 0]
        return res
def main():
    inp = input()
    global checked_name
    checked_name = input()
    DataSet(inp)
    data = getattr(DataSet, 'res')
    Statistics(data)
    


if __name__ == '__main__':
    main()

