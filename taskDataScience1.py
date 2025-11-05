import pandas as pd
import sys

def main(col_name, key, sort_by, ascending, file_path):
    vacancies = pd.read_csv(file_path)
    ascending = True if ascending == 'asc' else False

    mask = vacancies[col_name].str.contains(key, case=False, na=False)

    filtered = vacancies[mask].copy()

    filtered = filtered.reset_index()  
    filtered = filtered.sort_values(
        by=[sort_by, 'index'],
        ascending=[ascending, True]
    )

    print(filtered['name'].tolist())


def test():
    assert main('area_name', 'Москва', 'salary_from', 'asc', r'test/vacancies_small.csv')
try:
    if sys.argv[1] == 'test':
        test()
except IndexError:
    column = input()
    key = input()
    sort_by = input()
    ascending = input()
    main(column, key, sort_by, ascending, 'vacancies_small.csv')