from var_dump import var_dump
from prettytable import PrettyTable, ALL
import csv
import re
# main class - Vacancy and sec is Salary 
# vacancy => vacancy::name, ..., vacancy::Salary::salary_from
def cut_by_100(str):
    if len(str) > 100:
        return str[:100] + '...'
    else:
        return str
class Vacancy:
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
        
class Utils:
    @staticmethod
    def create_table(dataset):
        table = PrettyTable()
        table.field_names = ["№"] + [key for key, value in dataset[0].items()]
        table.align = "l"
        table.hrules = ALL
        for field in table.field_names:
            table.max_width[field] = 20
        for row in enumerate(dataset, start=1):
            res = [row[0]]
            for _, value in row[1].items():
                res.append(cut_by_100(value))
            table.add_row(res)
        print(table)
            
                

    

            
def main():
    inp = input()
    DataSet(inp)
    data = getattr(DataSet, 'res')
    Utils.create_table(data)
    pass
    


if __name__ == '__main__':
    main()