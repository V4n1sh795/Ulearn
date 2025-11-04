import pandas as pd

vacancies = pd.read_csv(r'test/vacancies_small.csv')

column = input()
key = input()
sort_by = input()
ascending = True if input() == 'asc' else False


column = vacancies[column]
column = column[column.str.contains(key, case=False)]

sort_by_column = vacancies[sort_by]
sort = sort_by_column.sort_values(ascending=ascending)

result = pd.DataFrame({'column': column, 'sort_by': sort, 'name': vacancies['name']})
result = (result 
    .dropna()
    .sort_values(by='sort_by', ascending=ascending)
)
print(result['name'].tolist())