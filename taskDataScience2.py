import pandas as pd
import sys
from collections import Counter



def main(vacancy, ascending, file_path):
    vacancies = pd.read_csv(file_path)
    ascending = True if ascending == 'asc' else False

    mask = vacancies['name'].str.contains(vacancy, case=False, na=False)
    result = [str.split('\r\n') for str in vacancies[mask]['key_skills'].dropna().tolist()]
    
    to_counter = []
    for elem0 in result:
        for elem1 in elem0:
            to_counter.append(elem1)

    to_sort_by_place = []
    for str in vacancies[mask]['key_skills'].dropna().tolist():
        for elem in str.split('\r\n'):
            to_sort_by_place.append(elem)
    
    result = Counter(to_counter)
    sorted_skills = dict(sorted(
        result.items(),
        key=lambda x: x[1],
        reverse=ascending    
    )[:5])
  
    not_to_remove = [item[0] for item in sorted_skills.items()]
    to_sort_by_place = [x for x in to_sort_by_place if x in not_to_remove]
    to_sort_by_place = list(dict.fromkeys(to_sort_by_place))
    df = pd.DataFrame({'pos': to_sort_by_place, 'skill': sorted_skills.keys(), 'nums': sorted_skills.values()})         
    df = df.reset_index().sort_values(
        by=['nums', 'index'],
        ascending=[ascending, True]
    )

    df = (df
          .drop(columns='pos')
          .drop(columns='index')
          )
    result = list(zip(df['skill'], df['nums']))
    print(result)
def test():
    assert main('программист', 'asc', r'test/vacancies_small.csv')
try:
    if sys.argv[1] == 'test':
        test() 
except IndexError:
    key = input()
    ascending = input()
    main(key, ascending, 'vacancies_small.csv')