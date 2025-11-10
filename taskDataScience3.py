import pandas as pd
import sys

def main(file_path, re):
    vacancies = pd.read_csv(file_path)
    df = vacancies[vacancies['salary_currency'] == 'RUR'].copy()
    df['middle_salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
    df = df.dropna(subset=['middle_salary'])

    df['middle_salary'] = df['middle_salary'].round(0).astype(int)
    
    city_avg = df.groupby('area_name')['middle_salary'].mean().round(0).astype(int)
    
    result_df = city_avg.reset_index()
    result_df = result_df.sort_values(
        by=['middle_salary', 'area_name'],
        ascending=[False, True]
    )
    
    result_dict = result_df.set_index('area_name')['middle_salary'].to_dict()
    
    print(result_dict)


def test():
    main(r'test/vacancies_small.csv', '\r\n')

try:
    if sys.argv[1] == 'test':
        test() 
except IndexError:
    main('vacancies_small.csv', '\n')