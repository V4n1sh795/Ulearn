import csv
from datetime import datetime

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


class Vacancy:
    def __init__(self, row):
        def check_name():
            global checked_name
            self.NameIn = True if checked_name.lower() in row['name'].lower() else False
        check_name()
        self.avg_salary = ((int(row['salary_from']) + int(row['salary_to']))//2) if row['salary_currency'] == 'Рубли' else (int(row['salary_from'])*(int( currency_to_rub[ row[salary_currency] ] )) + int(row['salary_to']) * (int( currency_to_rub[ row[salary_currency] ] )))//2
    pass


class Salary:
    pass


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
    @staticmethod
    def getyear(datatimestr):
        return int(datatimestr[-4:])
    
    def __init__(self, dataset):
        for row in dataset:
            v = Vacancy(row)




def main():
    inp = input()
    global checked_name
    checked_name = input()
    DataSet(inp)
    data = getattr(DataSet, 'res')
    statistics = Statistics(data)
    


if __name__ == '__main__':
    main()